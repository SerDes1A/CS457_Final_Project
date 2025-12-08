import logging
import os

LOG_PATH = os.path.join(os.path.dirname(__file__), "query.log")

logging.basicConfig(
    filename=LOG_PATH,
    filemode='a',
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def log_query(sql, params):
    logging.info(f"SQL: {sql} | PARAMS: {params}")