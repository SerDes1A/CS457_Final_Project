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

def update_task_status(task_id, new_status):
    valid_statuses = ['Not Started', 'In Progress', 'Complete']
    if new_status not in valid_statuses:
        raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
    
    sql = """
    UPDATE "Task"
    SET status = %s, updated_at = NOW()
    WHERE task_id = %s
    RETURNING *;
    """
    return execute(sql, (new_status, task_id), returning=True)

def update_task(task_id, title=None, description=None, due_date=None, priority=None):
    updates = []
    params = []
    
    if title is not None:
        updates.append("title = %s")
        params.append(title)
    if description is not None:
        updates.append("description = %s")
        params.append(description)
    if due_date is not None:
        updates.append("due_date = %s")
        params.append(due_date)
    if priority is not None:
        priority = priority.capitalize()
        valid_priorities = ['Low', 'Medium', 'High']
        if priority not in valid_priorities:
            priority = 'Medium'
        updates.append("priority = %s")
        params.append(priority)
    
    if not updates:
        return None
    
    updates.append("updated_at = NOW()")
    params.append(task_id)
    
    sql = f"""
    UPDATE "Task"
    SET {', '.join(updates)}
    WHERE task_id = %s
    RETURNING *;
    """
    
    return execute(sql, tuple(params), returning=True)