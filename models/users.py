from db_queries import fetch_one, fetch_all, execute

def create_user(email, pass_hash, first_name = None, last_name = None, role = "student"):
    sql = """
    INSERT INTO "User" (school_email, password, first_name, last_name, role)
    VALUES(%s, %s, %s, %s, %s)
    RETURNING *;
    """
    return execute(sql, (email, pass_hash, first_name, last_name, role), returning=True)

