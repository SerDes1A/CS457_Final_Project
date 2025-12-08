import psycopg
import logging

class Database:
    def __init__(self, host, dbname, user, password, port=5432):
        self.conn = psycopg.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )
    
    #allow for the execution of queries while logging them
    def executeQuery(self, query, params=None, fetch='all'):
        logging.info("Executing query: %s | parameters: %s", query.strip(), params)
        with self.conn.cursor() as cur:
            cur.execute(query,params or ())
            if fetch == 'one':
                return cur.fetchone()
            elif fetch == 'all':
                return cur.fetchall()
            return None
        
    def close(self):
        self.conn.close() #close the database connection