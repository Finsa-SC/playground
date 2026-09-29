class Database:
    def __init__(self, conn):
        self.conn = conn

    def execute(self, query: str, params: tuple | None = None, operation=None):
        with self.conn.cursor() as cur:
            cur.execute(query, params)
            if operation:
                return operation(cur, self.conn)

    def execute_query(self, query: str, params: tuple | None = None):
        return self.execute(
            query,
            params,
            lambda cur, conn: cur.fetchall()
        )

    def execute_non_query(self, query: str, params: tuple | None = None):
        return self.execute(
            query,
            params,
            lambda cur, conn: cur.rowcount
        )

    def execute_scalar(self, query: str, params: tuple | None = None):
        def _get_scalar(cur, conn):
            row = cur.fetchone()
            if row is None:
                return None
            return list(row.values())[0] if isinstance(row, dict) else row[0]

        return self.execute(query, params, _get_scalar)
