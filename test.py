import config
import resource

from hippo.pipeline import Pipeline


pipeline_config = config.PIPELINES['test_csv']
pipeline = Pipeline(pipeline_config)
pipeline.run()

pipeline_config = config.PIPELINES['test_parquet']
pipeline = Pipeline(pipeline_config)
pipeline.run()

pipeline_config = config.PIPELINES['test_json']
pipeline = Pipeline(pipeline_config)
pipeline.run()

usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
print(f'Memory usage (kB): {usage}')