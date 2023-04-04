import databases
import sqlalchemy

from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

metadata = sqlalchemy.MetaData()
database = databases.Database(f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
