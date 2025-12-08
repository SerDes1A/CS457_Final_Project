from db.db_queries import fetch_one, fetch_all, execute

def mark_attendance(event_id, user_id, status='Present'):
    valid_statuses = ['Present', 'Absent']
    if status not in valid_statuses:
        status_lower = status.lower()
        if status_lower in ['present', 'attended', 'here']:
            status = 'Present'
        elif status_lower in ['absent', 'missing', 'not here']:
            status = 'Absent'
        else:
            print(f"Warning: Invalid status '{status}'. Using 'Present'.")
            status = 'Present'
    
    # Check if record exists
    existing = fetch_one(
        'SELECT attendance_id FROM "Attendance" WHERE event = %s AND "user" = %s',
        (event_id, user_id)
    )
    
    if existing:
        # Update existing
        sql = """
        UPDATE "Attendance" 
        SET status = %s, time = NOW()
        WHERE event = %s AND "user" = %s
        RETURNING *;
        """
        return execute(sql, (status, event_id, user_id), returning=True)
    else:
        # Insert new
        sql = """
        INSERT INTO "Attendance" (event, "user", status, time)
        VALUES (%s, %s, %s, NOW())
        RETURNING *;
        """
        return execute(sql, (event_id, user_id, status), returning=True)

def list_event_attendance(event_id):
    sql = """
    SELECT a.*, u.first_name, u.last_name 
    FROM "Attendance" a JOIN "User" u ON a."user" = u.user_id
    WHERE a.event = %s
    ORDER BY u.last_name, u.first_name;
    """
    return fetch_all(sql, (event_id,))