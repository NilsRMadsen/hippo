# Hippo Data Ingestion

**WARNING**: *This project is in early prototyping/experimental development. The core philosophy and pipeline functionality are unlikely to change at this point, but the connectors are still under active development.*

Hippo is a modular configuration framework for data ingestion pipelines, using DuckDB (https://duckdb.org/) as the underlying query engine. The framework is intentionally designed to be extremely simple and intuitive to use for anyone familiar with Python. The goal is to make simple data pipelines very fast to set up, while still being flexible enough to accommodate the complex, bespoke logic often required in real-world data engineering.

The intended use case is single-node ingestion of small to medium size data. Where possible, Hippo uses DuckDB's built-in stream processing capabilities to process larger-than-memory files and data streams.

## Extractors and Loaders

Each pipeline is composed of one extractor and one loader, with an optional transformation step. Extractors and loaders are instances of connector classes.

Connector classes expose an ```extract``` method that returns a DuckDBPyRelation, and a ```load``` method that accepts a DuckDBPyRelation as input. When a connector is used as an extractor, the ```extract``` method will be called, and when it is used as a loader the ```load``` method will be called. Having this consistent interface allows us to freely mix-and-match connectors as extractors and loaders. 

**NOTE**: Some connectors won't implement both ```extract``` and ```load```, for example an API connector that is only intended for pulling data from a REST API and not writing to that API.

Example extractor and loader config:
```python
from hippo import connectors

PIPELINES = {
    'my_pipeline': {
        'extractor': {
            'class': connectors.FileConnector,
            'format': 'csv',
            'filepath': './data/raw.csv',
            'kwargs': {'header': True}   # passed to duckdb.read_csv()
        },
        'loader': {
            'class': connectors.FileConnector,
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
2. Any Python function that receives a DuckDBPyRelation as its first positional argument, and returns a DuckDBPyRelation, entered into the transformer config as ```'function': my_func```. This allows for the use of DuckDB's object-oriented Relational API. 

The transformer config is an optional component of the pipeline config. Omitting a transformer in the pipeline config will cause the data to pass unchanged from the extractor to the loader.

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

If both a query and a function are passed in the transformer config, the query will take priority, and the function will be ignored.

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

when the transformer config includes

```python
'kwargs': {'target_date': '2025-01-01'}
```


## One Pipeline Creates One Data Asset

A single Hippo pipeline should read from a single source, e.g. a single endpoint of an API, and create or update a single table or dataset. Sequential steps and fan-outs should be handled by executing multiple Hippo pipelines in the context of an orchestrator like Airflow, Dagster, or Prefect. Hippo does not have any built-in orchestration or dependency capabilities, nor is it intended to fill this role in the data stack.

## Dynamic Configuration

Unlike other configuration frameworks, Hippo uses native Python dictionaries in a ```config.py``` or similarly-named module to store pipeline configurations. This allows for dynamic insertion of configuration values, and for passing connector classes and transformer functions directly in the config.

## Running a Pipeline

When you want to run a pipeline, an instance of the ```hippo.pipeline.Pipeline``` class can be initialized by passing the pipeline config as the sole argument. Then, you simply have to call ```Pipeline.run()```:

```python
import config
from hippo.pipeline import Pipeline

pipeline_config = config.PIPELINES['my_pipeline']
pipeline = Pipeline(pipeline_config)
pipeline.run()
```

## Extensibility

Because of Hippo's dynamic configuration, it is very simple to extend its functionality with your own custom connector classes. For example, you can create a ```custom_connectors.py``` module in your project directory...

```python
from duckdb.duckdb import DuckDBPyRelation

class MyCustomConnector():
    def __init__(self, connector_config:dict) -> None:
        ...

    def extract(self) -> DuckDBPyRelation:
        ...

    def load(self, records:DuckDBPyRelation) -> None:
        ...
```

...then import this module into ```config.py```:

```python
from hippo import connectors
import custom_connectors

PIPELINES = {
    'my_pipeline': {
        'extractor': {
            'class': custom_connectors.MyCustomConnector,
            ...
        },
        ...
    }
}
```

The only requirement for a custom connector to work correctly as an extractor within the Hippo framework is for the connector class to expose an ```extract``` method that returns a DuckDBPyRelation.

The only requirement for a custom connector to work correctly as a loader within the Hippo framework is for the connector class to expose a ```load``` method that accepts a DuckDBPyRelation as its sole argument.

## Managing Secrets

Hippo implements a ```SecretsManager``` class to create and drop DuckDB temporary secrets in an object-oriented fashion:

```python
import config
from hippo.secrets import SecretsManager

secrets = SecretsManager(config.SECRETS)
secrets.create_all()
```

In ```config.py```:
```python
SECRETS = {
    's3_default': {
        'type': 's3',
        'provider': 'credential_chain',
    },
    ...
}
```

Hippo doesn't support creating persistent secrets, because DuckDB doesn't handle these in a secure fashion (secrets are persisted to an unencrypted file on disk.)

***IMPORTANT:*** It is strongly recommended not to hard-code credentials in the secrets config. Instead, you should dynamically insert these values into the config from an encrypted secrets store.

## Integration with Orchestrators

### Dagster

Since each pipeline extracts a single source into a single destination, Hippo pipelines fit naturally into Dagster's data asset philosophy. Creating a Dagster asset from a Hippo pipeline really is this easy:

```python
import config
import dagster as dg
from hippo.pipeline import Pipeline

@dg.asset
def my_data_asset():
    pipeline_config = config.PIPELINES['my_pipeline']
    pipeline = Pipeline(pipeline_config)
    pipeline.run()
```