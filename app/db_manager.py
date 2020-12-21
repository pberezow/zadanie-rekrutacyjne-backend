import psycopg2
import os


class DBManager:
    def __init__(self, db_config, test_db_config, is_test_instance, test_db_id=None):
        self._db_config = db_config
        self._test_db_config = test_db_config
        self._test_db_id = test_db_id
        self._is_test_instance = is_test_instance
        self._autocommit = True
        if is_test_instance:
            self.setup_test_manager()
        # print(self._connection)
        self._connection = self._get_db_url()
        self._db_connection = self._connect()
        self.init_db(db_config.get('init_script', None))

    def setup_test_manager(self):
        self._autocommit = True
        self.create_test_database()

    def create_test_database(self):
        base_url = self._test_db_config['database_url_base']
        conn = psycopg2.connect(dsn=base_url)
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

        # create database
        db_name = f'{self._test_db_config["test_table_prefix"]}_{self._test_db_id}'
        with conn.cursor() as curr:
            try:
                curr.execute(f'CREATE DATABASE {db_name};')
            except psycopg2.Error as err:
                raise RuntimeError() from err

        # connect manager to created db
        conn.close()
        self._connection = f'{base_url}{db_name}'
        try:
            self._db_connection = self._connect()
        except psycopg2.Error as err:
            raise RuntimeError() from err

        self.init_db(self._test_db_config['db_definition'])
        self._db_connection.close()
        return True

    def drop_test_db(self) -> bool:
        # close old connection and connect to db
        if self._db_connection:
            self._db_connection.close()

        base_url = self._test_db_config['database_url_base']
        conn = psycopg2.connect(dsn=base_url)
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

        db_name = f'{self._test_db_config["test_table_prefix"]}_{self._test_db_id}'
        with conn.cursor() as curr:
            try:
                curr.execute(f'DROP DATABASE {db_name};')
            except psycopg2.Error as err:
                raise RuntimeError() from err

        conn.close()
        return True

    def _connect(self):
        conn = psycopg2.connect(dsn=self._connection)
        conn.set_session(autocommit=self._autocommit)
        return conn

    def session(self):
        if self._db_connection.closed:
            self._db_connection = self._connect()
        return self._db_connection.cursor()
    
    def commit(self):
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
        if self._is_test_instance:
            return f'{self._test_db_config["database_url_base"]}{self._test_db_config["test_table_prefix"]}_{self._test_db_id}'
        else:
            return self._db_config['database_url']

    @staticmethod
    def prepare_uri(host: str, port: int, dbname: str, username: str = '', password: str = '',
                    engine: str = 'postgresql', **kwargs) -> str:
        connection_str = f'{engine}://{username}' + (f':{password}' if password else '') + ('@' if username else '') \
                         + f'{host}:{port}/{dbname}'
        return connection_str
