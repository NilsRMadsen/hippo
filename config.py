import transformers
from hippo import connectors


SECRETS = {

    's3_default': {
        'type': 's3',
        'provider': 'credential_chain',
    },

}


PIPELINES = {

    'test_read_write_csv': {
        'extractor': {
            'class': connectors.FileConnector,
            'format': 'csv',
            'filepath': './data/Electric_Vehicle_Population_Data.csv', #https://catalog.data.gov/dataset/electric-vehicle-population-data
        },
        'transformer': {
            'query_path': './transform_queries/test_csv.sql'
        },
        'loader': {
            'class': connectors.FileConnector,
            'format': 'csv',
            'filepath': './data/test_out.csv',
            'update_mode': 'overwrite',
        }
    },

    'test_write_new_file_csv': {
        'extractor': {
            'class': connectors.FileConnector,
            'format': 'csv',
            'filepath': './data/Electric_Vehicle_Population_Data.csv', #https://catalog.data.gov/dataset/electric-vehicle-population-data
        },
        'transformer': {
            'query_path': './transform_queries/test_csv.sql'
        },
        'loader': {
            'class': connectors.FileConnector,
            'format': 'csv',
            'filepath': './data/test_out.csv',
            'update_mode': 'new_file',
        }
    },

    'test_write_parquet': {
        'extractor': {
            'class': connectors.FileConnector,
            'format': 'csv',
            'filepath': './data/Electric_Vehicle_Population_Data.csv', #https://catalog.data.gov/dataset/electric-vehicle-population-data
        },
        'transformer': {
            'query_path': './transform_queries/test_csv.sql'
        },
        'loader': {
            'class': connectors.FileConnector,
            'format': 'parquet',
            'filepath': './data/test_out.parquet',
            'update_mode': 'overwrite',
        }
    },

    'test_write_new_file_parquet': {
        'extractor': {
            'class': connectors.FileConnector,
            'format': 'csv',
            'filepath': './data/Electric_Vehicle_Population_Data.csv', #https://catalog.data.gov/dataset/electric-vehicle-population-data
        },
        'transformer': {
            'query_path': './transform_queries/test_csv.sql'
        },
        'loader': {
            'class': connectors.FileConnector,
            'format': 'parquet',
            'filepath': './data/test_out.parquet',
            'update_mode': 'new_file',
        }
    },

    'test_write_json': {
        'extractor': {
            'class': connectors.FileConnector,
            'format': 'csv',
            'filepath': './data/Electric_Vehicle_Population_Data.csv', #https://catalog.data.gov/dataset/electric-vehicle-population-data
        },
        'transformer': {
            'query_path': './transform_queries/test_csv.sql'
        },
        'loader': {
            'class': connectors.FileConnector,
            'format': 'json',
            'filepath': './data/test_out.json',
            'update_mode': 'overwrite',
        }
    },

    'test_write_new_file_json': {
        'extractor': {
            'class': connectors.FileConnector,
            'format': 'csv',
            'filepath': './data/Electric_Vehicle_Population_Data.csv', #https://catalog.data.gov/dataset/electric-vehicle-population-data
        },
        'transformer': {
            'query_path': './transform_queries/test_csv.sql'
        },
        'loader': {
            'class': connectors.FileConnector,
            'format': 'json',
            'filepath': './data/test_out.json',
            'update_mode': 'new_file',
        }
    },

    'test_dynamic_query': {
        'extractor': {
            'class': connectors.FileConnector,
            'format': 'csv',
            'filepath': './data/Electric_Vehicle_Population_Data.csv', #https://catalog.data.gov/dataset/electric-vehicle-population-data
        },
        'transformer': {
            'query_path': './transform_queries/test_dynamic_query.sql',
            'kwargs': {'city': 'Seattle', 'state': 'WA'}
        },
        'loader': {
            'class': connectors.FileConnector,
            'format': 'csv',
            'filepath': './data/test_out_dynamic_query.csv',
            'update_mode': 'overwrite',
        }
    },

    'test_transform_func': {
        'extractor': {
            'class': connectors.FileConnector,
            'format': 'csv',
            'filepath': './data/Electric_Vehicle_Population_Data.csv', #https://catalog.data.gov/dataset/electric-vehicle-population-data
        },
        'transformer': {
            'function': transformers.test_func,
            'kwargs': {'limit': 1000, 'order_field': 'vin asc'}
        },
        'loader': {
            'class': connectors.FileConnector,
            'format': 'csv',
            'filepath': './data/test_out_func.csv',
            'update_mode': 'overwrite',
        }
    },

    'test_read_parquet': {
        'extractor': {
            'class': connectors.FileConnector,
            'format': 'parquet',
            'filepath': './data/test_out.parquet',
        },
        'transformer': {
            'query_path': './transform_queries/test_parquet.sql',
        },
        'loader': {
            'class': connectors.FileConnector,
            'format': 'json',
            'filepath': './data/test_read_parquet_out.json',
            'update_mode': 'overwrite',
            'kwargs': {'array': False, 'compression': 'gzip'}
        }
    },

    'test_read_json': {
        'extractor': {
            'class': connectors.FileConnector,
            'format': 'json',
            'filepath': './data/test_out.json',
            #'kwargs': {}
        },
        'transformer': {
            'query_path': './transform_queries/test_parquet.sql',
            #'kwargs': {}
        },
        'loader': {
            'class': connectors.FileConnector,
            'format': 'json',
            'filepath': './data/test_read_json_out.json',
            #'kwargs': {}
        }
    },

    'test_write_s3_csv': {
        'extractor': {
            'class': connectors.FileConnector,
            'format': 'csv',
            'filepath': './data/Electric_Vehicle_Population_Data.csv', #https://catalog.data.gov/dataset/electric-vehicle-population-data
        },
        'transformer': {
            'query_path': './transform_queries/test_csv.sql'
        },
        'loader': {
            'class': connectors.FileConnector,
            'format': 'csv',
            'filepath': 's3://nils-hippo-test/test_out.csv',
            'update_mode': 'overwrite',
            'secret_options': {
                'type': 's3',
                'provider': 'credential_chain',
            },
        }
    },

    'test_write_s3_parquet': {
        'extractor': {
            'class': connectors.FileConnector,
            'format': 'csv',
            'filepath': './data/Electric_Vehicle_Population_Data.csv', #https://catalog.data.gov/dataset/electric-vehicle-population-data
        },
        'transformer': {
            'query_path': './transform_queries/test_csv.sql'
        },
        'loader': {
            'class': connectors.FileConnector,
            'format': 'parquet',
            'filepath': 's3://nils-hippo-test/test_out.parquet',
            'update_mode': 'overwrite',
        }
    },

    'test_write_s3_json': {
        'extractor': {
            'class': connectors.FileConnector,
            'format': 'csv',
            'filepath': './data/Electric_Vehicle_Population_Data.csv', #https://catalog.data.gov/dataset/electric-vehicle-population-data
        },
        'transformer': {
            'query_path': './transform_queries/test_csv.sql'
        },
        'loader': {
            'class': connectors.FileConnector,
            'format': 'json',
            'filepath': 's3://nils-hippo-test/test_out.json',
            'update_mode': 'overwrite',
        }
    },

    'test_write_s3_parquet_newfile': {
        'extractor': {
            'class': connectors.FileConnector,
            'format': 'csv',
            'filepath': './data/Electric_Vehicle_Population_Data.csv', #https://catalog.data.gov/dataset/electric-vehicle-population-data
        },
        'transformer': {
            'query_path': './transform_queries/test_csv.sql'
        },
        'loader': {
            'class': connectors.FileConnector,
            'format': 'parquet',
            'filepath': 's3://nils-hippo-test/test_out.parquet',
            'update_mode': 'new_file',
        }
    },

    'test_read_write_s3_parquet': {
        'extractor': {
            'class': connectors.FileConnector,
            'format': 'parquet',
            'filepath': 's3://nils-hippo-test/test_out.parquet',
        },
        'transformer': {
            'query_path': './transform_queries/test_parquet.sql',
        },
        'loader': {
            'class': connectors.FileConnector,
            'format': 'csv',
            'filepath': 's3://nils-hippo-test/test_out_2.csv',
            'update_mode': 'overwrite'
        }
    },

}
