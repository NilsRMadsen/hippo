import duckdb

from hippo import utils


options = {
    'type': 's3',
    'provider': 'credential_chain',
}

options_str = utils.format_options(options)

duckdb.sql(f'''
    create or replace secret test (
        {options_str}
    );
''')

print(duckdb.sql('from duckdb_secrets();').fetchall())