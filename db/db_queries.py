from db.connection import db

def fetch_one(sql, params=None):
    return db.execute_query(sql, params, fetch="one")

def fetch_all(sql, params=None):
    return db.execute_query(sql, params, fetch="all")

def execute(sql, params=None, returning=False):
    result = db.execute_query(sql, params, fetch="one" if returning else None)
    db.conn.commit()
    return result