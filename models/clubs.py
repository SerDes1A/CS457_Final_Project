from db.db_queries import fetch_one, fetch_all, execute

#query creation for a default club
#information comes from create_club_service in club_service
def create_club(name, description=None, activity_status=None):
    sql = """
    INSERT INTO "Club" (name, description, activity_status, created_at)
    VALUES(%s, %s, %s, NOW())
    RETURNING *;
    """
    return execute(sql, (name, description, activity_status), returning=True)

#query to get a club by id
def get_club_by_id(club_id):
    sql = """
    SELECT * FROM "Club" WHERE club_id = %s;
    """
    return fetch_one(sql, (club_id,))

#query to get a club by name
def get_club_by_name(name):
    sql = """
    SELECT * FROM "Club" WHERE name = %s;
    """
    return fetch_one(sql, (name,))

#query to get all clubs
def list_clubs():
    sql = """
    SELECT * FROM "Club"
    ORDER BY club_id
    """
    return fetch_all(sql)

#query to update club information 
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
    SET """ + ', '.join(parts) + """ WHERE club_id = %s 
    RETURNING *;
    """
    return execute(sql, tuple(params), returning=True)