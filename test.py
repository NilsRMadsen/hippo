import config
import resource
from hippo.pipeline import Pipeline


for pipeline_config in config.PIPELINES.values():
    pipeline = Pipeline(pipeline_config)
    pipeline.run()

usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
print(f'Memory usage (kB): {usage}')