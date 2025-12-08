from db_queries import fetch_one, fetch_all, execute

def create_event(club_id, name, description, start_datetime, end_datetime, location):
    sql = """
    INSERT INTO "Events" (club_id, name, description, start_datetime, end_datetime, location)
    VALUES (%s, %s, %s, %s, %s, %s)
    RETURNING *;
    """
    return execute(sql, (club_id, name, description, start_datetime, end_datetime, location), returning=True)

def get_event(event_id):
    sql = """
    SELECT * FROM "Events" 
    WHERE event_id = %s;
    """
    return fetch_one(sql, (event_id,))

def list_events_for_club(club_id):
    sql = """
    SELECT * FROM "Events" 
    WHERE club_id = %s
    ORDER BY start_datetime;
    """
    return fetch_all(sql, (club_id,))