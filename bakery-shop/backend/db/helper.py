from contextlib import contextmanager
from .database import Database
from .pool import pool

@contextmanager
def transaction():
    with pool.connection() as conn:
        yield Database(conn)
