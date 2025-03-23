from . import utils

import duckdb
import os
import re

from duckdb.duckdb import DuckDBPyRelation
from pathlib import Path


class FileLoader():
    '''
    A loader for writing data to files in local storage or cloud object storage.
    '''
    valid_formats = {'csv', 'parquet', 'json'}
    valid_update_modes = {'overwrite', 'new_file'}

    def __init__(self, loader_config:dict) -> None:
        self.loader_config = loader_config
        self.kwargs = loader_config.get('kwargs', dict())

        # file format
        try:
            self.format = loader_config['format']
        except KeyError:
            raise KeyError(f'Loader config must specify a "format".')

        if self.format not in self.valid_formats:
            raise ValueError(f'"{self.format}" is not a valid file format. Valid formats are {self.valid_formats}')

        # file path and file system
        try:
            self.filepath = loader_config['filepath']
        except KeyError:
            raise KeyError(f'Loader config must specify a "filepath".')

        if re.match(r'^s3:', self.filepath):
            self.file_system = 's3'
        elif re.match(r'^gs:', self.filepath):
            self.file_system = 'gcs'
        elif re.match(r'^(?:az|azure):', self.filepath):
            self.file_system = 'azure_blob'
        else:
            self.file_system = 'local'

        # update mode
        self.update_mode = loader_config.get('update_mode', 'overwrite')
        if self.update_mode not in self.valid_update_modes:
            raise ValueError(f'"{self.update_mode}" is not a valid update mode. Valid update modes are {self.valid_update_modes}')

        # credentials
        self.creds = loader_config.get('creds')


    def create_secret(self) -> None:
        if self.file_system == 's3':
            if not self.creds:
                duckdb.sql('''
                create or replace secret s3_loader (
                    type s3,
                    provider credential_chain
                );
                ''')


    def load(self, records:DuckDBPyRelation) -> None:
        self.create_secret()

        if self.update_mode == 'overwrite':
            path_str = self.filepath
        elif self.update_mode == 'new_file':
            path_str = utils.add_uuid_to_filename(self.filepath)

        try:
            if self.format == 'csv':
                records.to_csv(path_str, **self.kwargs)
            elif self.format == 'parquet':
                records.to_parquet(path_str, **self.kwargs)
            elif self.format == 'json':
                duckdb.sql(f"copy records to '{path_str}';")

        except Exception as e:
            # if anything goes wrong during file write, delete the file fragment
            if self.update_mode == 'new_file':
                if self.file_system == 'local' and Path(path_str).exists():
                    os.remove(path_str)
            raise e

