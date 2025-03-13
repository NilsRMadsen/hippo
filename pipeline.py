import config
import duckdb
import time

from duckdb.duckdb import DuckDBPyRelation
from pathlib import Path


class Pipeline():
    def __init__(self, pipeline_config:dict) -> None:
        self.pipeline_config = pipeline_config

        extractor_class = self.pipeline_config['extractor']['class']
        self.extractor = extractor_class(self.pipeline_config['extractor'])

        self.transform_query = self.pipeline_config.get('transform_query')

        loader_class = self.pipeline_config['loader']['class']
        self.loader = loader_class(self.pipeline_config['loader'])


    def extract(self) -> DuckDBPyRelation:
        return self.extractor.extract()


    def transform(self, records:DuckDBPyRelation) -> DuckDBPyRelation:
        if not self.transform_query:
            return records
        
        else:
            query_path = (Path(config.TRANSFORM_QUERY_PATH) / self.transform_query).resolve()
            
            with open(query_path, 'r') as f:
                tquery = f.read()

            clean_records = duckdb.sql(tquery)
            return clean_records


    def load(self, records:DuckDBPyRelation) -> None:
        self.loader.load(records)


    def run(self) -> None:
        start_time = time.time()

        records = self.extract()
        clean_records = self.transform(records)
        self.load(clean_records)

        end_time = time.time()
        print('Run complete.\n')
        print(f'Time elapsed: {round(end_time - start_time, 3)} seconds\n')
