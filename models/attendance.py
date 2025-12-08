from db_queries import fetch_one, fetch_all, execute

def mark_attendance(event_id, user_id, status='attended'):
    sql = """
    INSERT INTO "Attendance" (event_id, user_id, status)
    VALUES (%s, %s, %s)
    ON CONFLICT (event_id, user_id) DO UPDATE SET status = EXCLUDED.status, time=now()
    RETURNING *;
    """
    return execute(sql, (event_id, user_id, status), returning=True)

def list_event_attendance(event_id):
    sql = """
    SELECT a.*, u.first_name, u.last_name 
    FROM "Attendance" a JOIN "Users" u ON a.user_id = u.user_id
    WHERE a.event_id = %s;
    """
    return fetch_all(sql, (event_id,))