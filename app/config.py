import os
import multiprocessing


app_config = {
    'db': {
        'engine': 'postgres',
        'username': os.environ.get('POSTGRES_USER', 'postgres'),
        'password': os.environ.get('POSTGRES_PASSWORD', 'postgres'),
        'host': os.environ.get('POSTGRES_HOST', 'localhost'),
        'port': int(os.environ.get('POSTGRES_PORT', '5432')),
        'dbname': os.environ.get('POSTGRES_DB_NAME', 'app_db'),
        'init_script': './app/tables.sql'
    },
    'gunicorn': {
        'reload': False,
        'loglevel': 'debug',
        'errorlog': 'gunicorn.error.log',
        'accesslog': 'gunicorn.log',
        'capture_output': True,
        'workers': multiprocessing.cpu_count() * 2 + 1,
        'proc_name': 'gunicorn_application',
        'bind': [
            '0.0.0.0:8000'
        ]
    }
}
