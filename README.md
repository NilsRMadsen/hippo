## Hippo Data Ingestion

This package implements a pipeline-as-config framework for data ingestion pipelines, using DuckDB (https://duckdb.org/) as the underlying query engine.

### Extractors and Loaders

Each pipeline is composed of one extractor and one loader, with an optional transformation step. Transformations in Hippo are defined as DuckDB SQL queries.

Every extractor class exposes an ```extract``` method that returns a DuckDB relation. Similarly, every loader class exposes a ```load``` method that accepts a DuckDB relation as input. Having this consistent interface allows us to freely mix-and-match extractors and loaders.

### Integration with Dagster

Since each pipeline loads a single source into a single destination, Hippo pipelines fit naturally into Dagster's data asset paradigm. Creating a Dagster asset from a hippo pipeline is really this easy:

```
import config
import dagster as dg
from hippo.pipeline import Pipeline

@dg.asset
def my_data_asset():
    pipeline_config = config.PIPELINES['my_pipeline_name']
    pipeline = Pipeline(pipeline_config)
    pipeline.run()
```