import psycopg
from psycopg import rows
import logging

class Database:
    def __init__(self, host, dbname, user, password, port=5432):
        self.conn = psycopg.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password,
            row_factory=rows.dict_row  # Set it here
        )
    
    def execute_query(self, query, params=None, fetch='all'):
        logging.info("Executing query: %s | parameters: %s", query.strip(), params)
        with self.conn.cursor() as cur:
            cur.execute(query, params or ())
            if fetch == 'one':
                return cur.fetchone()
            elif fetch == 'all':
                return cur.fetchall()
            return None
    
    def close(self):
        self.conn.close()

db = Database(
    host="localhost",
    port=5432,
    dbname="CS457_Final",
    user="postgres",
    password="D@t@_1"
)

