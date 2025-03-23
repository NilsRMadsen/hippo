from . import utils

import duckdb

from duckdb.duckdb import DuckDBPyRelation


class FileConnector():
    '''
    A connector for reading from and writing to files in local storage or cloud 
    object storage.
    '''
    valid_formats = {'csv', 'json', 'parquet'}
    valid_update_modes = {'overwrite', 'new_file'}


    def __init__(self, connector_config:dict) -> None:
        self.connector_config = connector_config
        self.kwargs = connector_config.get('kwargs', dict())

        # get file format
        try:
            self.format = connector_config['format']
        except KeyError:
            raise KeyError(f'FileConnector config must specify a "format".')

        if self.format not in self.valid_formats:
            raise ValueError(f'"{self.format}" is not a valid file format. Valid formats are {self.valid_formats}')
        
        # get file path(s)
        try:
            self.filepath = connector_config['filepath']
        except KeyError:
            raise KeyError(f'FileConnector config must specify a "filepath".')

        # update mode
        self.update_mode = connector_config.get('update_mode', 'overwrite')
        if self.update_mode not in self.valid_update_modes:
            raise ValueError(f'"{self.update_mode}" is not a valid update mode. Valid update modes are {self.valid_update_modes}')


    def extract(self) -> DuckDBPyRelation:

        if self.format == 'csv':
            records = duckdb.read_csv(self.filepath, **self.kwargs)
        elif self.format == 'json':
            records = duckdb.read_json(self.filepath, **self.kwargs)
        elif self.format == 'parquet':
            records = duckdb.read_parquet(self.filepath, **self.kwargs)
        
        return records


    def load(self, records:DuckDBPyRelation) -> None:

        if self.update_mode == 'overwrite':
            path_str = self.filepath
        elif self.update_mode == 'new_file':
            if isinstance(self.filepath, list):
                path_str = [utils.add_uuid_to_filename(fp) for fp in self.filepath]
            else:
                path_str = utils.add_uuid_to_filename(self.filepath)

        if self.format == 'csv':
            records.to_csv(path_str, **self.kwargs)
        elif self.format == 'json':
            if self.kwargs:
                duckdb.sql(f"copy records to '{path_str}' ({utils.format_options(self.kwargs)});")
            else:
                duckdb.sql(f"copy records to '{path_str}';")
        elif self.format == 'parquet':
            records.to_parquet(path_str, **self.kwargs)
        