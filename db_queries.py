from .connection import get_connection

def fetch_one(sql, params=None):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params or())
            return cur.fetchone()
        
def fetch_all(sql, params=None):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params or())
            return cur.fetchall()
        
def execute(sql, params=None, returning=False):
    with get_connection() as conn:
        with conn.cursor()as cur:
            cur.execute(sql, params or())
            if returning:
                return cur.fetchone()
            conn.commit()