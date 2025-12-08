from db.connection import get_connection
from logger import log_query

def fetch_one(sql, params=None):
    log_query(sql, params)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params or())
            return cur.fetchone()
        
def fetch_all(sql, params=None):
    log_query(sql, params)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params or())
            return cur.fetchall()
        
def execute(sql, params=None, returning=False):
    log_query(sql, params)
    with get_connection() as conn:
        with conn.cursor()as cur:
            cur.execute(sql, params or())
            if returning:
                return cur.fetchone()
            conn.commit()