from db.db_queries import fetch_one, fetch_all, execute

def create_task(club_id, title, description = None, due_date = None, priority = 'Medium'):
    if priority:
        priority = priority.capitalize()
        valid_priorities = ['Low', 'Medium', 'High']
        if priority not in valid_priorities:
            print(f"Warning: Invalid priority '{priority}'. Using 'Medium'.")
            priority = 'Medium'
    
    sql = """
    INSERT INTO "Task" (club, title, description, due_date, created_at, updated_at, priority, status)
    VALUES (%s, %s, %s, %s, NOW(), NOW(), %s, 'Not Started')
    RETURNING *;
    """
    return execute(sql, (club_id, title, description, due_date, priority), returning=True)

def get_task(task_id):
    sql = """
    SELECT * FROM "Task"
    WHERE task_id = %s;
    """
    return fetch_one(sql, (task_id,))

def list_tasks(club_id):
    sql = """
    SELECT * FROM "Task"
    WHERE club_id = %s
    ORDER BY due_date;
    """
    return fetch_all(sql, (club_id,))