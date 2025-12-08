from db.db_queries import fetch_one, fetch_all, execute

def create_club(name, description=None, activity_status=None):
    sql = """
    INSERT INTO "Club" (name, description, activity_status, created_at)
    VALUES(%s, %s, %s, NOW())
    RETURNING *;
    """
    return execute(sql, (name, description, activity_status), returning=True)

def get_club_by_id(club_id):
    sql = """
    SELECT * FROM "Club" WHERE club_id = %s;
    """
    return fetch_one(sql, (club_id,))

def get_club_by_name(name):
    sql = """
    SELECT * FROM "Club" WHERE name = %s;
    """
    return fetch_one(sql, (name,))

def list_clubs():
    sql = """
    SELECT * FROM "Club"
    ORDER BY name
    """
    return fetch_all(sql)

def update_club_info(club_id, name=None, description=None, activity_status=None):
    parts = []
    params = []
    
    if name is not None:
        parts.append("name = %s")
        params.append(name)
    if description is not None:
        parts.append("description = %s")
        params.append(description)
    if activity_status is not None:
        parts.append("activity_status = %s")
        params.append(activity_status)
    
    if not parts:
        return None
    
    params.append(club_id)
    
    sql = """
    UPDATE "Club" 
    SET """ + ', '.join(parts) + """
    WHERE club_id = %s 
    RETURNING *;
    """
    return execute(sql, tuple(params), returning=True)