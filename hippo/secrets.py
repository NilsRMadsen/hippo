from . import utils

import duckdb


class SecretsManager():
    '''
    A class for creating and dropping temporary, in-memory DuckDB secrets from a 
    secrets config dictionary.
    '''

    def __init__(self, secrets_config:dict) -> None:
        self.secrets_config = secrets_config


    def create_secret(self, name:str) -> None:
        try:
            secret_dict = self.secrets_config[name]
        except KeyError:
            raise KeyError(f'"{name}" is not a key in the secrets config.')

        duckdb.sql(f'''
            create or replace temporary secret {name} (
                {utils.format_options(secret_dict)}
            )
        ''')


    def create_all(self) -> None:
        '''
        Creates all secrets in the secrets config.
        '''
        for name in self.secrets_config.keys():
            self.create_secret(name)

    
    def drop_secret(self, name:str) -> None:
        '''
        Drops a single named secret.
        '''
        duckdb.sql(f'drop secret {name};')

    
    def drop_all(self) -> None:
        '''
        Drops all secrets in the secrets config.
        '''
        for name in self.secrets_config.keys():
            self.drop_secret(name)
