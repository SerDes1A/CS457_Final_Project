from models.clubs import create_club, list_clubs, get_club_by_id, get_club_by_name, update_club_info
from models.club_membership import(
    add_membership_direct, add_membership_request,
    get_membership, list_memberships,
    get_pending_requests, approve_membership, update_membership_role,
    remove_membership
)
from config import OFFICER_ROLES

def check_officer(user, club_id):
    m = get_membership(club_id, user["user_id"])
    return bool(m and m["is_active"] and m["role"] in OFFICER_ROLES)

def list_out_clubs():
    rows = list_clubs()
    for r in rows:
        print(f"{r['club_id']:4} | {r['name']} - {r.get('activity_status') or ''}")

def create_club_service(current_user):
    name = input("Club name: ").strip()
    if get_club_by_name(name):
        print("Club already exists.")
        return None
    description = input("Description: ").strip()
    activity_status = input("Activity Status: ").strip() or None
    club = create_club(name, description, activity_status)
    print("Created Club: ", club["club_id"], club["name"])
    add_membership_direct(club["club_id"], current_user["user_id"], role="president")
    print("You were added as president of the club.")
    return club

def join_club_request(current_user):
    list_out_clubs()
    club_id = int(input("Club ID to request: ").strip())
    existing = get_membership(club_id, current_user["user_id"])
    if existing:
            if existing["is_active"]:
                 print("Already an active member.")
            else:
                 print("Membership request already pending.")
            return
    add_membership_request(club_id, current_user["user_id"])
    print("Membership request recorded. Awaiting approval by officers.")

def list_memberships_for_club(club_id):
     rows = list_memberships(club_id)
     for r in rows:
        status = "active" if r["is_active"] else "pending"
        print(f"{r['membership_id']:4} | {r['userid']:4} | {r.get('first_name')} {r.get('last_name')} | role: {r['role']} | {status}")

def list_pending_requests(user, club_id):
    if not check_officer(user, club_id):
        print("Must be an officer to list pending requests.")
        return
    rows = get_pending_requests(club_id)
    if not rows:
        print("No pending requests for this club.")
        return
    for r in rows:
        print(f"{r['membership_id']:4} | {r['userid']:4} | {r.get('first_name')} {r.get('last_name')} | {r['school_email']}")

def approve_membership(user, club_id):
    if not check_officer(user, club_id):
        print("Must be an officer to approve memberships.")
        return
    # Show pending requests first
    rows = get_pending_requests(club_id)
    if not rows:
        print("No pending requests for this club.")
        return
    print("Pending requests:")
    for r in rows:
        print(f"  User ID: {r['userid']} - {r.get('first_name')} {r.get('last_name')} ({r['school_email']})")

    user_id = int(input("User ID to approve: ").strip())
    role = input("Role to assign (member/officer/etc): ").strip() or "member"
    rec = approve_membership(club_id, user_id, role)
    if rec:
        print("Approved membership:", rec["membership_id"], "role:", rec["role"])
    else:
        print("No pending request found for that user.")
        
def promote_member(user, club_id):
    if not check_officer(user, club_id):
        print("Must be an officer to change roles.")
        return
    # Show current members
    rows = list_memberships(club_id)
    print("Current members:")
    for r in rows:
        status = "active" if r["is_active"] else "pending"
        print(f"  User ID: {r['userid']} - {r.get('first_name')} {r.get('last_name')} ({r['role']}, {status})")
    
    user_id = int(input("User ID to promote/demote: ").strip())
    new_role = input("New role (member/officer/president/treasurer/secretary): ").strip()
    rec = update_membership_role(club_id, user_id, new_role)
    if rec:
        print("Updated role: ", rec["userid"], "=>", rec["role"])
    else:
        print("No membership found.")


def remove_member(user, club_id):
    if not check_officer(user, club_id):
        print("Must be an officer to remove members.")
        return
    # Show current members
    rows = list_memberships(club_id)
    print("Current members:")
    for r in rows:
        status = "active" if r["is_active"] else "pending"
        print(f"  User ID: {r['userid']} - {r.get('first_name')} {r.get('last_name')} ({r['role']}, {status})")
    
    user_id = int(input("User ID to remove: ").strip())
    rec = remove_membership(club_id, user_id)
    if rec:
        print("Removed membership of user:", user_id)
    else:
        print("No membership found.")

def update_club_info_service(user, club_id):
    if not check_officer(user, club_id):
        print("Must be an officer to update club info.")
        return
    name = input("New name (leave blank to keep): ").strip() or None
    description = input("New description (leave blank to keep): ").strip() or None
    status = input("New activity status (leave blank to keep): ").strip() or None
    rec = update_club_info(club_id, name, description, status)
    if rec:
        print("Updated club:", rec["club_id"], rec["name"])
    else:
        print("No changes made.")