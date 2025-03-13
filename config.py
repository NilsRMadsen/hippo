from hippo import extractors, loaders


PIPELINES = {

    'test_csv': {
        'extractor': {
            'class': extractors.LocalFileExtractor,
            'format': 'csv',
            'filepath': './data/Electric_Vehicle_Population_Data.csv', #https://catalog.data.gov/dataset/electric-vehicle-population-data
            #'kwargs': {}
        },
        'transform_query': './transform_queries/test_csv.sql',
        'loader': {
            'class': loaders.LocalFileLoader,
            'format': 'parquet',
            'filepath': './data/test_out.parquet',
            'update_mode': 'overwrite',
            #'kwargs': {}
        }
    },

    'test_parquet': {
        'extractor': {
            'class': extractors.LocalFileExtractor,
            'format': 'parquet',
            'filepath': './data/test_out.parquet',
            #'kwargs': {}
        },
        'transform_query': './transform_queries/test_parquet.sql',
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
        'transform_query': './transform_queries/test_parquet.sql',
        'loader': {
            'class': loaders.LocalFileLoader,
            'format': 'csv',
            'filepath': './data/test_out_2.csv',
            #'kwargs': {}
        }
    }

}
