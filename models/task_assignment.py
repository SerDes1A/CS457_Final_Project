from db.db_queries import fetch_one, fetch_all, execute

def assign_task(task_id, user_id):
    sql = """
    INSERT INTO "Task Assignment" (task, "user", assigned_at)
    VALUES (%s, %s, NOW())
    RETURNING *;
    """
    return execute(sql, (task_id, user_id), returning=True)

def list_assignments_by_user(user_id):
    sql = """
    SELECT ta.*, t.title 
    FROM "Task Assignment" ta JOIN "Task" t
    On ta.task = t.task_id WHERE ta."user" = %s;
    """
    return fetch_all(sql, (user_id,))