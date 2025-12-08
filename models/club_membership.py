from db.db_queries import fetch_one, fetch_all, execute

def add_membership_request(clubid, userid, role='member'):
    sql="""
    INSERT INTO "Club Membership" (clubid, userid, role, is_active, dues_paid)
    VALUES (%s, %s, %s, false, false)
    RETURNING *;
    """
    return execute(sql, (clubid, userid, role), returning=True)

def add_membership_direct(clubid, userid, role='member'):
    sql = """
    INSERT INTO "Club Membership" (clubid, userid, role, is_active, dues_paid)
    VALUES (%s, %s, %s, true, false)
    RETURNING *;
    """
    return execute(sql, (clubid, userid, role), returning=True)

def get_membership(clubid, userid):
    sql = """
    SELECT * FROM "Club Membership"
    WHERE clubid = %s AND userid = %s;
    """
    return fetch_one(sql, (clubid, userid))

def list_memberships(clubid):
    sql = """
    SELECT cm.*, u.first_name, u.last_name, u.school_email
    FROM "Club Membership" cm JOIN "User" u 
    ON cm.userid = u.user_id WHERE cm.clubid = %s;
    """
    return fetch_all(sql, (clubid,))

def get_pending_requests(clubid):
    sql = """
    SELECT cm.*, u.first_name, u.last_name, u.school_email
    FROM "Club Membership" cm JOIN "User" u
    ON cm.userid = u.user_id WHERE cm.clubid = %s AND cm.is_active = false;
    """
    return fetch_all(sql, (clubid,))

def approve_membership(club_id, user_id, role='member'):
    sql = """UPDATE "Club Membership" SET is_active = true, role = %s WHERE clubid = %s AND userid = %s RETURNING *;"""
    return execute(sql, (role, club_id, user_id), returning=True)

def update_membership_role(clubid, userid, new_role):
    sql = """
    UPDATE "Club Membership"
    SET role = %s
    WHERE clubid = %s AND userid = %s
    RETURNING *;
    """
    return execute(sql, (new_role, clubid, userid), returning=True)

def remove_membership(clubid, userid):
    sql = """
    DELETE FROM "Club Membership"
    WHERE clubid = %s AND userid = %s
    RETURNING *;
    """
    return execute(sql, (clubid, userid), returning=True)

def mark_dues_paid(club_id, user_id):
    """Mark a member's dues as paid"""
    sql = """
    UPDATE "Club Membership"
    SET dues_paid = true
    WHERE clubid = %s AND userid = %s
    RETURNING *;
    """
    return execute(sql, (club_id, user_id), returning=True)

def mark_dues_unpaid(club_id, user_id):
    """Mark a member's dues as unpaid"""
    sql = """
    UPDATE "Club Membership"
    SET dues_paid = false
    WHERE clubid = %s AND userid = %s
    RETURNING *;
    """
    return execute(sql, (club_id, user_id), returning=True)