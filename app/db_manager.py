import psycopg2
import os


class DBManager:
    def __init__(self, db_config):
        self._db_config = db_config
        self._connection = self._get_db_url()
        self._db_connection = self._connect()
        self.init_db(db_config.get('init_script', None))

    def _connect(self):
        conn = psycopg2.connect(dsn=self._connection)
        conn.set_session(autocommit=True)
        return conn

    def session(self):
        if self._db_connection.closed:
            self._db_connection = self._connect()
        return self._db_connection.cursor()
    
    def commit(self, autocommit=True):
        self._db_connection.commit()

    def rollback(self):
        self._db_connection.rollback()

    def init_db(self, init_script):
        if init_script is not None:
            with open(init_script, 'r') as file:
                script = file.read()

            lines = script.split('\n')
            lines = [line for line in lines if not line.startswith('--') and line != '']
            queries = filter(lambda q: q != '', '\n'.join(lines).split(';'))
            with self.session() as cur:
                for query in queries:
                    cur.execute(query)
                self.commit()
    
    def _get_db_url(self):
        return self._db_config['database_url']

    @staticmethod
    def prepare_uri(host: str, port: int, dbname: str, username: str = '', password: str = '',
                    engine: str = 'postgresql', **kwargs) -> str:
        connection_str = f'{engine}://{username}' + (f':{password}' if password else '') + ('@' if username else '') \
                         + f'{host}:{port}/{dbname}'
        return connection_str
