from db_queries import fetch_one, fetch_all, execute

def add_file(club_id, source_url, event_id=None):
    sql = """
    INSERT INTO "File Resource" (club_id, event_id, source_url)
    VALUES (%s, %s, %s)
    RETURNING*;
    """
    return execute(sql, (club_id, event_id, source_url), returning=True)

def list_files(club_id):
    sql = """
    SELECT * FROM "File Resource" 
    WHERE club_id = %s
    ORDER BY created_at DESC;
    """
    return fetch_all(sql, (club_id,))