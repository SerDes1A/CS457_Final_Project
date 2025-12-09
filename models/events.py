from db.db_queries import fetch_one, fetch_all, execute

#query to create a new event
def create_event(club_id, name, description, start_datetime, end_datetime, location):
    sql = """
    INSERT INTO "Event" (club, name, description, start_datetime, end_datetime, location, created_at)
    VALUES (%s, %s, %s, %s, %s, %s, NOW())
    RETURNING *;
    """
    return execute(sql, (club_id, name, description, start_datetime, end_datetime, location), returning=True)

#query to get an event using the id
def get_event(event_id):
    sql = """
    SELECT * FROM "Event" 
    WHERE event_id = %s;
    """
    return fetch_one(sql, (event_id,))

#query to get all events a club has
def list_events_for_club(club_id):
    sql = """
    SELECT * FROM "Event" 
    WHERE club = %s
    ORDER BY start_datetime;
    """
    return fetch_all(sql, (club_id,))