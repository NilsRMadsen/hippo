import duckdb
from duckdb.duckdb import DuckDBPyRelation


def test_func(records:DuckDBPyRelation, limit:int, order_field:str) -> DuckDBPyRelation:
    col_list = [
        duckdb.ColumnExpression('VIN (1-10)').alias('vin'),
        duckdb.ColumnExpression('County').alias('county'),
        duckdb.ColumnExpression('City').alias('city'),
        duckdb.ColumnExpression('State').alias('state'),
        duckdb.ColumnExpression('Postal Code').alias('postal_code'),
    ]

    return records.select(*col_list).limit(limit).order(order_field)
