import config
import duckdb
import resource

from hippo.pipeline import Pipeline
from hippo.secrets import SecretsManager


if __name__ == '__main__':
    # create all configured DuckDB secrets
    secrets = SecretsManager(config.SECRETS)
    secrets.create_all()

    # run all configured pipelines
    for name, pipeline_config in config.PIPELINES.items():
        print(f'Running pipeline "{name}"')
        pipeline = Pipeline(pipeline_config)
        pipeline.run()

    usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print(f'Memory usage (kB): {usage}')