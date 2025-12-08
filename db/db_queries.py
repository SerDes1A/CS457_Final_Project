from db.connection import db
import logging

def fetch_one(sql, params=None):
    logging.info("fetch_one: %s | parameters: %s", sql.strip(), params)
    return db.execute_query(sql, params, fetch="one")

def fetch_all(sql, params=None):
    logging.info("fetch_all: %s | parameters: %s", sql.strip(), params)
    return db.execute_query(sql, params, fetch="all")

def execute(sql, params=None, returning=False):
    logging.info("execute: %s | parameters: %s", sql.strip(), params)
    result = db.execute_query(sql, params, fetch="one" if returning else None)
    db.conn.commit()
    return result