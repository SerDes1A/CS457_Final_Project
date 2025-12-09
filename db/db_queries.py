from db.connection import db
import logging

logging.basicConfig(
    filename="appQueries.log",
    level=logging.INFO,
    format="%(asctime)s %(message)s"
)

def fetch_one(sql, params=None):
    logging.info("fetch_one: %s | parameters: %s", sql.strip(), params)
    return db.execute_query(sql, params, fetch="one")

def fetch_all(sql, params=None):
    logging.info("fetch_all: %s | parameters: %s", sql.strip(), params)
    return db.execute_query(sql, params, fetch="all")

def execute(sql, params=None, returning=False):
    logging.info("execute: %s | parameters: %s", sql.strip(), params)
    try:
        result = db.execute_query(sql, params, fetch="one" if returning else None)
        db.conn.commit()
        return result
    except Exception as e:
        logging.error("Execute failed: %s", e)
        db.conn.rollback()  # Rollback on error
        raise