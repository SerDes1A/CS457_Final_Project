from db.db_queries import fetch_one, fetch_all, execute

def mark_attendance(event_id, user_id, status='attended'):
    status_map = {
        'present': 'Present',
        'absent': 'Absent',
        'attended': 'Present',  # Map 'attended' to 'Present'
        'attendance': 'Present'
    }
    
    status_lower = status.lower()
    if status_lower in status_map:
        status_enum = status_map[status_lower]
    else:
        print(f"Warning: Invalid status '{status}'. Using 'Present'.")
        status_enum = 'Present'
    
    sql = """
    INSERT INTO "Attendance" (event, "user", status, time)
    VALUES (%s, %s, %s, NOW())
    ON CONFLICT (event, "user") DO UPDATE SET status = EXCLUDED.status, time=NOW()
    RETURNING *;
    """
    return execute(sql, (event_id, user_id, status_enum), returning=True)

def list_event_attendance(event_id):
    sql = """
    SELECT a.*, u.first_name, u.last_name 
    FROM "Attendance" a JOIN "User" u ON a."user" = u.user_id
    WHERE a.event = %s;
    """
    return fetch_all(sql, (event_id,))