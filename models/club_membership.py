from db.db_queries import fetch_one, fetch_all, execute

#query to add a user as a member of a club
#used in join_club_request in club_service when requesting
def add_membership_request(clubid, userid, role='member'):
    sql="""
    INSERT INTO "Club Membership" (clubid, userid, role, is_active, dues_paid)
    VALUES (%s, %s, %s, false, false)
    RETURNING *;
    """
    return execute(sql, (clubid, userid, role), returning=True)

#query to add a user a member directly
#used in create_club_service in club_service where it creates a user as the president
def add_membership_direct(clubid, userid, role='member'):
    sql = """
    INSERT INTO "Club Membership" (clubid, userid, role, is_active, dues_paid)
    VALUES (%s, %s, %s, true, false)
    RETURNING *;
    """
    return execute(sql, (clubid, userid, role), returning=True)

#query to find a user's membership in a club
def get_membership(clubid, userid):
    sql = """
    SELECT * FROM "Club Membership"
    WHERE clubid = %s AND userid = %s;
    """
    return fetch_one(sql, (clubid, userid))

#query to get all memberships of a club
def list_memberships(clubid):
    sql = """
    SELECT cm.*, u.first_name, u.last_name, u.school_email
    FROM "Club Membership" cm JOIN "User" u 
    ON cm.userid = u.user_id WHERE cm.clubid = %s;
    """
    return fetch_all(sql, (clubid,))

def get_user_memberships(userid):
    sql = """
    SELECT cm.*, c.name FROM "Club Membership" cm
    JOIN "Club" c ON cm.clubid = c.club_id
    WHERE cm.userid = %s
    """
    return fetch_all(sql, (userid,))

#query to get pending membership requests
def get_pending_requests(clubid):
    sql = """
    SELECT cm.*, u.first_name, u.last_name, u.school_email
    FROM "Club Membership" cm JOIN "User" u
    ON cm.userid = u.user_id WHERE cm.clubid = %s AND cm.is_active = false;
    """
    return fetch_all(sql, (clubid,))

#query to add membership to a user 
def approve_membership(club_id, user_id, role='member'):
    sql = """UPDATE "Club Membership" SET is_active = true, role = %s WHERE clubid = %s AND userid = %s RETURNING *;"""
    return execute(sql, (role, club_id, user_id), returning=True)

#query to change the role of a member in a club
def update_membership_role(clubid, userid, new_role):
    sql = """
    UPDATE "Club Membership"
    SET role = %s
    WHERE clubid = %s AND userid = %s
    RETURNING *;
    """
    return execute(sql, (new_role, clubid, userid), returning=True)

#query to remove a member
def remove_membership(clubid, userid):
    sql = """
    DELETE FROM "Club Membership"
    WHERE clubid = %s AND userid = %s
    RETURNING *;
    """
    return execute(sql, (clubid, userid), returning=True)

#query to update a user's dues as paid (true)
def mark_dues_paid(club_id, user_id):
    sql = """
    UPDATE "Club Membership"
    SET dues_paid = true
    WHERE clubid = %s AND userid = %s
    RETURNING *;
    """
    return execute(sql, (club_id, user_id), returning=True)

#query to update a user's dues as unpaid (false)
def mark_dues_unpaid(club_id, user_id):
    sql = """
    UPDATE "Club Membership"
    SET dues_paid = false
    WHERE clubid = %s AND userid = %s
    RETURNING *;
    """
    return execute(sql, (club_id, user_id), returning=True)