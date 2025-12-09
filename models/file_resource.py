from db.db_queries import fetch_one, fetch_all, execute

#query to add a file
def add_file(club_id, source_url, name):
    sql = """
    INSERT INTO "File Resource" (club, source_url, created_at, name)
    VALUES (%s, %s, NOW(), %s)
    RETURNING*;
    """
    return execute(sql, (club_id, name, source_url), returning=True)

#query to list out files
def list_files_for_club(club_id):
    sql = """
    SELECT * FROM "File Resource" 
    WHERE club = %s
    ORDER BY created_at DESC;
    """
    return fetch_all(sql, (club_id,))