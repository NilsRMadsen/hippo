# Hippo Data Ingestion

**NOTE**: This project is in very early prototyping/experimental development. Anything in this project could change from this point on, including the underlying query engine.

Hippo is a modular configuration framework for data ingestion pipelines, using DuckDB (https://duckdb.org/) as the underlying query engine. 

The intended use case is single-node data ingestion of small to medium size data. Where feasible, Hippo uses DuckDB's built-in stream processing capabilities to process larger-than-memory files and data streams.

## Extractors and Loaders

Each pipeline is composed of one extractor and one loader, with an optional transformation step.

Every extractor class exposes an ```extract``` method that returns a DuckDBPyRelation. Similarly, every loader class exposes a ```load``` method that accepts a DuckDBPyRelation as input. Having this consistent interface allows us to freely mix-and-match extractors and loaders.

Example extractor and loader config:
```python
from hippo import extractors, loaders

PIPELINES = {
    'my_pipeline': {
        'extractor': {
            'class': extractors.LocalFileExtractor,
            'format': 'csv',
            'filepath': './data/raw.csv',
            'kwargs': {'header': True}   # passed to duckdb.read_csv()
        },
        'loader': {
            'class': loaders.LocalFileLoader,
            'format': 'parquet',
            'filepath': './data/out.parquet',
            'update_mode': 'overwrite',
            # the kwargs entry is optional
        }
    }
}
```

## Transformers

A transformer in Hippo can be either:
1. A DuckDB SQL query, entered into the transformer config as ```'query_path': 'path/to/query.sql'```. The query should initially refer to a relation named ```records``` and return a single result set, e.g. ```select a, b from records```.
2. Any Python function that receives a DuckDBPyRelation as its first positional argument, and returns a DuckDBPyRelation, entered into the transformer config as ```'function': my_func```. This allow for usage of DuckDB's object-oriented Relational API. 

Adding a ```'kwargs': {...}``` entry to the transformer config will expand the functionality based the type of transformer. For functions, ```kwargs``` will simply be passed into the function as additional keyword arguments. For queries, ```kwargs``` can be used to make the query dynamic. Entries in ```kwargs``` will be used to format the SQL query string using Python's ```str.format()``` method. 

For example:

```sql
select a, b, event_date
from records
where
    event_date = '{target_date}'
```

will be converted to

```sql
select a, b, event_date
from records
where
    event_date = '2025-01-01'
```

when the transformer config also includes

```python
'kwargs': {'target_date': '2025-01-01'}
```

The transformer config is an optional component of the pipeline config. Omitting a transformer in the pipeline config will cause the data to pass unchanged from the extractor to the loader.

If both a query and a function are passed in the transformer config, the query will take priority, and the function will be ignored.

Example transformer config:
```python
import my_transformers

PIPELINES = {
    'my_pipeline': {
        'extractor': {...},
        'transformer': {
            'query_path': 'example/query.sql',
            'function': my_transformers.my_func,  # ignored here
            'kwargs': {'arg_1': 'value_1'}  # dynamically replaces {arg_1} in the query with value_1 using str.format(**kwargs)
        },
        'loader': {...}
    }
}
```

## One Pipeline Creates One Data Asset

A single Hippo pipeline should read from a single source, e.g. a single endpoint of an API, and create or update a single table or dataset. Sequential steps and fan-outs should be handled by executing multiple Hippo pipelines in the context of an orchestrator like Airflow, Dagster, or Prefect. Hippo does not have any built-in orchestration or dependency capabilities, nor is it intended to fill this role in the data stack.

## Dynamic Configuration

Unlike other configuration frameworks, Hippo uses native Python dictionaries in a ```config.py``` or similarly-named module to store configurations. This allows for dynamic insertion of configuration values, and the passing of extractor and loader classes directly in the config. When you want to run a pipeline, an instance of the Pipeline class can be initialized by passing the pipeline config dictionary as the sole argument.

## Extensibility

Because of Hippo's dynamic configuration, it is very simple to extend its functionality with your own custom extractors and loaders. For example, you can create a ```custom_extractors.py``` module in your project directory...

```python
from hippo.extractors import HippoExtractor

class MyCustomExtractor(HippoExtractor):
    def __init__(extractor_config:dict) -> None:
        super().__init__(extractor_config)
        ...
```

...then import this module into ```config.py```:

```python
from hippo import extractors, loaders
import custom_extractors

PIPELINES = {
    'my_pipeline': {
        'extractor': {
            'class': custom_extractors.MyCustomExtractor,
            ...
        },
        ...
    }
}
```

The only requirements for a custom extractor to work correctly within the Hippo framework is for the extractor to inherit from the HippoExtractor base class, pass the extractor config to ```super().__init__``` in the child's ```__init__``` method, and expose an ```extract``` method that returns a DuckDBPyRelation.

The only requirements for a custom loader to work correctly within the Hippo framework is for the loader to inherit from the HippoLoader base class, pass the loader config to ```super().__init__``` in the child's ```__init__``` method, and expose a ```load``` method that accepts a DuckDBPyRelation as its sole argument.

## Integration with Orchestrators

### Dagster

Since each pipeline extracts a single source into a single destination, Hippo pipelines fit naturally into Dagster's data asset paradigm. Creating a Dagster asset from a Hippo pipeline is really this easy:

```python
import config
import dagster as dg
from hippo.pipeline import Pipeline

@dg.asset
def my_data_asset():
    pipeline_config = config.PIPELINES['my_pipeline_name']
    pipeline = Pipeline(pipeline_config)
    pipeline.run()
```