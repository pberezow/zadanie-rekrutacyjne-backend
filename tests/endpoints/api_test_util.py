import pytest
from falcon import testing

from app.application import Application


_app_config = {
    'db': {
        'engine': 'postgres',
        'username': 'postgres',
        'password': 'postgres',
        'host': 'localhost',
        'port': 5432,
        'dbname': 'app_db',
        'init_script': './app/tables.sql',
        'database_url': 'postgres://postgres:postgres@localhost:5432/app_db'
    },
    'test_db': {
        'database_url_base': 'postgres://postgres:postgres@localhost:5432/',
        'test_table_prefix': 'test_app_db',
        'db_definition': './app/tables.sql'
    }
}


def _get_client_with_unique_db():
    indices = [0]

    def func():
        indices.append(indices[-1] + 1)
        return testing.TestClient(Application(_app_config, is_test_instance=True, test_db_id=indices[-1]))

    return func


app_instance = _get_client_with_unique_db()
