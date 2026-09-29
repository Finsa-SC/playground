import os
from dotenv import load_dotenv
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

load_dotenv()

conninfo = os.getenv(
    "DATABASE_URL",
    f"host={os.getenv('POSTGRES_HOST', 'localhost')} "
    f"port={os.getenv('POSTGRES_PORT', '5432')} "
    f"dbname={os.getenv('POSTGRES_DB')} "
    f"user={os.getenv('POSTGRES_USER')} "
    f"password={os.getenv('POSTGRES_PASSWORD')}"
)

pool = ConnectionPool(
    conninfo=conninfo,
    min_size=int(os.getenv("DB_POOL_MIN", 1)),
    max_size=int(os.getenv("DB_POOL_MAX", 10)),
    open=False,
    kwargs={
        "connect_timeout": 5,
        "row_factory": dict_row
    }
)
