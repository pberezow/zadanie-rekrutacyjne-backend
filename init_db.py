from app.db_manager import DBManager
from app.config import app_config

if __name__ == '__main__':
    manager = DBManager(app_config.get('db', {}))
    manager.init_db('./app/tables.sql')
