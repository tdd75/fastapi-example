import dotenv

from app.config.logging import config_logging
from app.config.setting import Setting
from app.db.session import ConnectionPool

dotenv.load_dotenv()
setting = Setting()
config_logging(setting)
connection_pool = ConnectionPool(setting.DB_URL)

__all__ = [
    'setting',
    'connection_pool',
]
