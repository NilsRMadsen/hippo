import transformers
from hippo import extractors, loaders


PIPELINES = {

    'test_read_write_csv': {
        'extractor': {
            'class': extractors.LocalFileExtractor,
            'format': 'csv',
            'filepath': './data/Electric_Vehicle_Population_Data.csv', #https://catalog.data.gov/dataset/electric-vehicle-population-data
        },
        'transformer': {
            'query_path': './transform_queries/test_csv.sql'
        },
        'loader': {
            'class': loaders.LocalFileLoader,
            'format': 'csv',
            'filepath': './data/test_out.csv',
            'update_mode': 'overwrite',
        }
    },

    'test_write_new_file_csv': {
        'extractor': {
            'class': extractors.LocalFileExtractor,
            'format': 'csv',
            'filepath': './data/Electric_Vehicle_Population_Data.csv', #https://catalog.data.gov/dataset/electric-vehicle-population-data
        },
        'transformer': {
            'query_path': './transform_queries/test_csv.sql'
        },
        'loader': {
            'class': loaders.LocalFileLoader,
            'format': 'csv',
            'filepath': './data/test_out.csv',
            'update_mode': 'new_file',
        }
    },

    'test_write_parquet': {
        'extractor': {
            'class': extractors.LocalFileExtractor,
            'format': 'csv',
            'filepath': './data/Electric_Vehicle_Population_Data.csv', #https://catalog.data.gov/dataset/electric-vehicle-population-data
        },
        'transformer': {
            'query_path': './transform_queries/test_csv.sql'
        },
        'loader': {
            'class': loaders.LocalFileLoader,
            'format': 'parquet',
            'filepath': './data/test_out.parquet',
            'update_mode': 'overwrite',
        }
    },

    'test_write_new_file_parquet': {
        'extractor': {
            'class': extractors.LocalFileExtractor,
            'format': 'csv',
            'filepath': './data/Electric_Vehicle_Population_Data.csv', #https://catalog.data.gov/dataset/electric-vehicle-population-data
        },
        'transformer': {
            'query_path': './transform_queries/test_csv.sql'
        },
        'loader': {
            'class': loaders.LocalFileLoader,
            'format': 'parquet',
            'filepath': './data/test_out.parquet',
            'update_mode': 'new_file',
        }
    },

    'test_write_json': {
        'extractor': {
            'class': extractors.LocalFileExtractor,
            'format': 'csv',
            'filepath': './data/Electric_Vehicle_Population_Data.csv', #https://catalog.data.gov/dataset/electric-vehicle-population-data
        },
        'transformer': {
            'query_path': './transform_queries/test_csv.sql'
        },
        'loader': {
            'class': loaders.LocalFileLoader,
            'format': 'json',
            'filepath': './data/test_out.json',
            'update_mode': 'overwrite',
        }
    },

    'test_write_new_file_json': {
        'extractor': {
            'class': extractors.LocalFileExtractor,
            'format': 'csv',
            'filepath': './data/Electric_Vehicle_Population_Data.csv', #https://catalog.data.gov/dataset/electric-vehicle-population-data
        },
        'transformer': {
            'query_path': './transform_queries/test_csv.sql'
        },
        'loader': {
            'class': loaders.LocalFileLoader,
            'format': 'json',
            'filepath': './data/test_out.json',
            'update_mode': 'new_file',
        }
    },

    'test_dynamic_query': {
        'extractor': {
            'class': extractors.LocalFileExtractor,
            'format': 'csv',
            'filepath': './data/Electric_Vehicle_Population_Data.csv', #https://catalog.data.gov/dataset/electric-vehicle-population-data
        },
        'transformer': {
            'query_path': './transform_queries/test_dynamic_query.sql',
            'kwargs': {'city': 'Seattle', 'state': 'WA'}
        },
        'loader': {
            'class': loaders.LocalFileLoader,
            'format': 'csv',
            'filepath': './data/test_out_dynamic_query.csv',
            'update_mode': 'overwrite',
        }
    },

    'test_transform_func': {
        'extractor': {
            'class': extractors.LocalFileExtractor,
            'format': 'csv',
            'filepath': './data/Electric_Vehicle_Population_Data.csv', #https://catalog.data.gov/dataset/electric-vehicle-population-data
        },
        'transformer': {
            'function': transformers.test_func,
            'kwargs': {'limit': 1000, 'order_field': 'vin asc'}
        },
        'loader': {
            'class': loaders.LocalFileLoader,
            'format': 'csv',
            'filepath': './data/test_out_func.csv',
            'update_mode': 'overwrite',
        }
    },

    'test_read_parquet': {
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
            'filepath': './data/test_read_parquet_out.json',
            'update_mode': 'overwrite',
            #'kwargs': {'separators': (', ', ': ')}
        }
    },

    'test_read_json': {
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
            'format': 'json',
            'filepath': './data/test_read_json_out.json',
            #'kwargs': {}
        }
    }

}
