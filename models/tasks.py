from db_queries import fetch_one, fetch_all, execute

def create_task(club_id, title, description = None, due_date = None, priority = None):
    sql = """
    INSERT INTO "Tasks" (club_id, title, description, due_date, priority)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING *;
    """
    return execute(sql, (club_id, title, description, due_date, priority), returning=True)

def get_task(task_id):
    sql = """
    SELECT * FROM "Tasks"
    WHERE task_id = %s;
    """
    return fetch_one(sql, (task_id,))

def list_tasks(club_id):
    sql = """
    SELECT * FROM "Tasks"
    WHERE club_id = %s
    ORDER BY due_date;
    """
    return fetch_all(sql, (club_id,))