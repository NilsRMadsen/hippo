import duckdb
import time
from duckdb.duckdb import DuckDBPyRelation
from pathlib import Path


class Pipeline():
    def __init__(self, pipeline_config:dict) -> None:
        self.pipeline_config = pipeline_config

        extractor_class = self.pipeline_config['extractor']['class']
        self.extractor = extractor_class(self.pipeline_config['extractor'])

        self.transformer = self.pipeline_config.get('transformer')

        loader_class = self.pipeline_config['loader']['class']
        self.loader = loader_class(self.pipeline_config['loader'])


    def extract(self) -> DuckDBPyRelation:
        return self.extractor.extract()


    def transform(self, records:DuckDBPyRelation) -> DuckDBPyRelation:
        if not self.transformer:
            return records
        
        elif 'query_path' in self.transformer:
            query_path = Path(self.transformer['query_path']).resolve()
            query_format_values = self.transformer.get('kwargs')
            
            with open(query_path, 'r') as f:
                tquery = f.read()

            if isinstance(query_format_values, dict):
                tquery = tquery.format(**query_format_values)

            clean_records = duckdb.sql(tquery)
            return clean_records
        
        elif 'function' in self.transformer:
            transform_func = self.transformer['function']
            transform_kwargs = self.transformer.get('kwargs', dict())

            if callable(transform_func):
                clean_records = transform_func(records, **transform_kwargs)
            else:
                raise ValueError(f'The value passed in transformer.function is not a callable Python object.')

            if isinstance(clean_records, DuckDBPyRelation):
                return clean_records
            else:
                raise TypeError(f'The transformer function must return a DuckDBPyRelation. Got {type(clean_records)}')

        else:
            raise ValueError(f'The transformer config must specify a "query_path" or "function" key.')


    def load(self, records:DuckDBPyRelation) -> None:
        self.loader.load(records)


    def run(self) -> None:
        start_time = time.time()

        records = self.extract()
        clean_records = self.transform(records)
        self.load(clean_records)

        end_time = time.time()
        print('Run complete.')
        print(f'Time elapsed: {round(end_time - start_time, 3)} seconds\n')
