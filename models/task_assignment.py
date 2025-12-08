from db.db_queries import fetch_one, fetch_all, execute

def assign_task(task_id, user_id):
    sql = """
    INSERT INTO "Task Assignment" (task_id, user_id)
    VALUES (%s, %s)
    RETURNING *;
    """
    return execute(sql, (task_id, user_id), returning=True)

def list_assignments_by_user(user_id):
    sql = """
    SELECT ta.*, t.title 
    FROM "Task Assignment" ta JOIN "Tasks" t
    On ta.task_id = t.task_id WHERE ta.user_id = %s;
    """
    return fetch_all(sql, (user_id,))