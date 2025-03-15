import transformers
from hippo import extractors, loaders


PIPELINES = {

    'test_csv': {
        'extractor': {
            'class': extractors.LocalFileExtractor,
            'format': 'csv',
            'filepath': './data/Electric_Vehicle_Population_Data.csv', #https://catalog.data.gov/dataset/electric-vehicle-population-data
        },
        'transformer': {
            'query_path': './transform_queries/test_csv.sql',
            'kwargs': {'city': 'Seattle', 'state': 'WA'}
        },
        'loader': {
            'class': loaders.LocalFileLoader,
            'format': 'csv',
            'filepath': './data/test_out.csv',
            'update_mode': 'overwrite',
        }
    },

    'test_csv_func': {
        'extractor': {
            'class': extractors.LocalFileExtractor,
            'format': 'csv',
            'filepath': './data/Electric_Vehicle_Population_Data.csv', #https://catalog.data.gov/dataset/electric-vehicle-population-data
        },
        'transformer': {
            'function': transformers.test_csv,
            'kwargs': {}
        },
        'loader': {
            'class': loaders.LocalFileLoader,
            'format': 'parquet',
            'filepath': './data/test_out.parquet',
            'update_mode': 'overwrite',
        }
    },

    'test_parquet': {
        'extractor': {
            'class': extractors.LocalFileExtractor,
            'format': 'parquet',
            'filepath': './data/test_out.parquet',
        },
        'transformer': {
            'query_path': './transform_queries/test_parquet.sql',
        },
        'loader': {
            'class': loaders.LocalFileLoader,
            'format': 'json',
            'filepath': './data/test_out.json',
            'update_mode': 'overwrite',
            #'kwargs': {'separators': (', ', ': ')}
        }
    },

    'test_json': {
        'extractor': {
            'class': extractors.LocalFileExtractor,
            'format': 'json',
            'filepath': './data/test_out.json',
            #'kwargs': {}
        },
        'transformer': {
            'query_path': './transform_queries/test_parquet.sql',
            #'kwargs': {}
        },
        'loader': {
            'class': loaders.LocalFileLoader,
            'format': 'csv',
            'filepath': './data/test_out_2.csv',
            #'kwargs': {}
        }
    }

}
