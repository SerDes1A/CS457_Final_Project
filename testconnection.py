# test_connection.py
import psycopg

try:
    conn = psycopg.connect(
        host="localhost",
        dbname="CS457_Final",
        user="postgres",
        password="D@t@_1"  # Try empty string first
    )
    print("✓ Connection successful!")
    
    # Test a simple query
    with conn.cursor() as cur:
        cur.execute("SELECT version();")
        version = cur.fetchone()
        print(f"✓ PostgreSQL version: {version[0]}")
    
    conn.close()
except Exception as e:
    print(f"✗ Connection failed: {e}")