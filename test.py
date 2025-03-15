import config
import resource
from hippo.pipeline import Pipeline


for name, pipeline_config in config.PIPELINES.items():
    print(f'Running pipeline "{name}"')
    pipeline = Pipeline(pipeline_config)
    pipeline.run()

usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
print(f'Memory usage (kB): {usage}')