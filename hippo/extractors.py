import duckdb
from duckdb.duckdb import DuckDBPyRelation
from pathlib import Path


class LocalFileExtractor():
    '''
    An extractor for reading data from local files.
    '''
    valid_formats = {'csv', 'json', 'parquet'}


    def __init__(self, extractor_config:dict) -> None:
        self.extractor_config = extractor_config
        self.kwargs = extractor_config.get('kwargs', dict())

        self.format = extractor_config['format']
        if self.format not in self.valid_formats:
            raise ValueError(f'"{self.format}" is not a valid file format')
        
        self.filepath = str(Path(extractor_config['filepath']).resolve())


    def extract(self) -> DuckDBPyRelation:
        if self.format == 'csv':
            records = duckdb.read_csv(self.filepath, **self.kwargs)

        elif self.format == 'json':
            records = duckdb.read_json(self.filepath, **self.kwargs)

        elif self.format == 'parquet':
            records = duckdb.read_parquet(self.filepath, **self.kwargs)
        
        return records
