import resource

from pipeline import Pipeline


pipeline = Pipeline('test_csv')
pipeline.run()

pipeline = Pipeline('test_parquet')
pipeline.run()

# pipeline = Pipeline('test_json')
# pipeline.run()

usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
print(f'Memory usage (kB): {usage}')