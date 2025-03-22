from . import utils

import duckdb
import os
from duckdb.duckdb import DuckDBPyRelation
from pathlib import Path


class LocalFileLoader():
    '''
    A loader for writing data to local files.
    '''
    valid_formats = {'csv', 'parquet', 'json'}
    valid_update_modes = {'overwrite', 'new_file'}


    def __init__(self, loader_config:dict) -> None:
        self.loader_config = loader_config
        self.kwargs = loader_config.get('kwargs', dict())

        try:
            self.format = loader_config['format']
        except KeyError:
            raise KeyError(f'Loader config must specify a "format".')

        if self.format not in self.valid_formats:
            raise ValueError(f'"{self.format}" is not a valid file format. Valid formats are {self.valid_formats}')

        try:
            self.filepath = Path(loader_config['filepath']).resolve()
        except KeyError:
            raise KeyError(f'Loader config must specify a "filepath".')

        self.update_mode = loader_config.get('update_mode', 'overwrite')
        if self.update_mode not in self.valid_update_modes:
            raise ValueError(f'"{self.update_mode}" is not a valid update mode. Valid update modes are {self.valid_update_modes}')


    def load(self, records:DuckDBPyRelation) -> None:
        if self.update_mode == 'overwrite':
            path_str = str(self.filepath)
        elif self.update_mode == 'new_file':
            unique_path = utils.add_uuid_to_path(self.filepath)
            path_str = str(unique_path)

        try:
            if self.format == 'csv':
                records.to_csv(path_str, **self.kwargs)
            elif self.format == 'parquet':
                records.to_parquet(path_str, **self.kwargs)
            elif self.format == 'json':
                duckdb.sql(f"copy records to '{path_str}';")

        except Exception as e:
            # if anything goes wrong during file write, delete the file fragment to ensure atomicity
            if self.update_mode == 'new_file' and unique_path.exists():
                os.remove(unique_path)
            raise e
