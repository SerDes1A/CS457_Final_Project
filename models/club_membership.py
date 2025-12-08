from db_queries import fetch_one, fetch_all, execute

def add_membership_request(club_id, user_id, role='member'):
    sql="""
    INSERT INTO "Club Membership" (club_id, user_id, role, is_active)
    VALUES (%s, %s, %s, false)
    RETURNING *;
    """
    return execute(sql, (club_id, user_id, role), returning=True)

def add_membership_direct(club_id, user_id, role='member'):
    sql = """
    INSERT INTO "Club Membership" (club_id, user_id, role, is_active)
    VALUES (%s, %s, %s, true)
    RETURNING *;
    """
    return execute(sql, (club_id, user_id, role), returning=True)

def get_membership(club_id, user_id):
    sql = """
    SELECT * FROM "Club Membership"
    WHERE club_id = %s AND user_id = %s;
    """
    return fetch_one(sql, (club_id, user_id))

def list_memberships(club_id):
    sql = """
    SELECT cm.*, u.first_name, u.last_name, u.school_email
    FROM "Club Membership" cm JOIN "Users" u 
    ON cm.user_id = u.user_id WHERE cm.club_id = %s;
    """
    return fetch_all(sql, (club_id,))

def get_pending_requests(club_id):
    sql = """
    SELECT cm.*, u.first_name, u.last_name, u.school_email
    FROM "Club Membership" cm JOIN "Users" u
    ON cm.user_id = u.user_id WHERE cm.club_id = %s AND cm.is_active = false;
    """
    return fetch_all(sql, (club_id,))

def approve_membership(club_id, user_id, role='member'):
    sql = """
    UPDATE "Club Membership" 
    SET is_active=true, role = %s, joined_at = now()
    WHERE club_id = %s AND user_id = %s
    RETURNING *;
    """
    return execute(sql, (role, club_id, user_id), returning=True)

def update_membership_role(club_id, user_id, new_role):
    sql = """
    UPDATE "Club Membership"
    SET role = %s 
    WHERE club_id = %s AND user_id = %s
    RETURNING *;
    """
    return execute(sql, (new_role, club_id, user_id), returning=True)

def remove_membership(club_id, user_id):
    sql = """
    DELETE FROM "Club Membership"
    WHERE club_id = %s AND user_id = %s
    RETURNING *;
    """
    return execute(sql, (club_id, user_id), returning=True)