from models.clubs import create_club, list_clubs, get_club_by_id, get_club_by_name, update_club_info
from models.club_membership import(
    add_membership_direct, add_membership_request,
    get_membership, list_memberships, get_user_memberships,
    get_pending_requests, approve_membership, update_membership_role,
    remove_membership, mark_dues_paid, mark_dues_unpaid
)
from input_validation import confirm_action
from config import OFFICER_ROLES


#check if the user is an officer
#***works***
def check_officer(user, club_id):
    m = get_membership(club_id, user["user_id"])
    return bool(m and m["is_active"] and m["role"] in OFFICER_ROLES)

#lists out all clubs found in the "Clubs" table
#***works***
def list_out_clubs():
    rows = list_clubs()
    for r in rows:
        print(f"{r['club_id']:4} | {r['name']} - {r.get('activity_status') or ''}")

def list_out_user_clubs(user):
    clubs = get_user_memberships(user['user_id'])
    if not clubs:
        print("\nYou are not a member of any clubs.")
    else:
        from display import display_table
        display_data = []
        for r in clubs:
            status = "✅ Active" if r["is_active"] else "⏳ Pending"
            role_display = r["role"].title() if r["role"] else "Member"
            
            display_data.append({
                'Club ID': r['clubid'],
                'Club Name': r['name'],
                'Your Role': role_display,
                'Status': status
            })
        display_table(display_data, ['Club ID', 'Club Name', 'Your Role', 'Status'])

#interactive service for creating a club
#***works***
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

#allow users to request to join a club
#***works***
def join_club_request(current_user):
    list_out_clubs() #get list of clubs
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

#allow user to view memberships to a clubs (active or pending)
#***works***
def list_memberships_for_club(club_id):
     rows = list_memberships(club_id)
     for r in rows:
        status = "active" if r["is_active"] else "pending"
        print(f"{r['membership_id']:4} | {r['userid']:4} | {r.get('first_name')} {r.get('last_name')} | role: {r['role']} | {status}")

#officer tool - approve memberships for users who requested membership
#***works***
def approve_membership_service(user, club_id):
    if not check_officer(user, club_id):
        print("Must be an officer to approve memberships.")
        return
    
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

#officer tool - officer can promote/demote a member 
#changes privleges of user if they change from officer -> member 
#***works***
def promote_member(user, club_id):
    if not check_officer(user, club_id):
        print("Must be an officer to change roles.")
        return
    
    rows = list_memberships(club_id)
    print("Current members:")
    for r in rows:
        status = "active" if r["is_active"] else "pending"
        print(f"  User ID: {r['userid']} - {r.get('first_name')} {r.get('last_name')} ({r['role']}, {status})")
    
    user_id = int(input("User ID to promote/demote (0 to cancel): ").strip())
    if user_id == 0:
        return 
    
    new_role = input("New role (member/officer/president/treasurer/secretary): ").strip()

    if user_id == user["user_id"]:
        print("\n You are changing YOUR OWN role!")
        print(f"Current role: {next((r['role'] for r in rows if r['userid'] == user_id), 'unknown')}")
        print(f"New role: {new_role}")

    current_membership = get_membership(club_id, user_id)
    if current_membership and current_membership['role'] in OFFICER_ROLES and new_role.lower() == 'member':
        print("\nWARNING: You are demoting yourself from officer to member!")
        print("You will lose officer privileges for this club immediately.")
        
        confirm = input("Are you absolutely sure? (type 'yes' to confirm): ").strip().lower()
        if confirm != 'yes':
            print("Role change cancelled.")
            return

    rec = update_membership_role(club_id, user_id, new_role)
    if rec:
        print("Updated role: ", rec["userid"], "=>", rec["role"])
    else:
        print("No membership found.")

#officer tools - allows an officer to remove a member
#can't remove themselves/another officer without changing their role first
#***works***
def remove_member(user, club_id):
    if not check_officer(user, club_id):
        print("Must be an officer to remove members.")
        return
    
    rows = list_memberships(club_id)
    print("Current members:")
    for r in rows:
        status = "active" if r["is_active"] else "pending"
        print(f"  User ID: {r['userid']} - {r.get('first_name')} {r.get('last_name')} ({r['role']}, {status})")
    
    user_id = int(input("User ID to remove (0 to cancel): ").strip())
    if user_id == "0":
        return
    current_membership = get_membership(club_id, user_id)
    if current_membership and current_membership['role'] in OFFICER_ROLES:
        print("This member has an officer role and cannot be removed")
        print("The role will have to be changed before being removed.")
        return
    if user_id == user["user_id"]:
        print("\nWARNING: You will be removing yourself from the club!")
        print("You will need to request membership to the club to have access again.")
        
        confirm = input("Are you absolutely sure? (type 'yes' to confirm): ").strip().lower()
        if confirm != 'yes':
            print("Membership removal canceled.")
            return
        
    rec = remove_membership(club_id, user_id)
    if rec:
        print("Removed membership of user:", user_id)
    else:
        print("No membership found.")

#officer tools - allow to update the information of a club
#***works***
def update_club_info_service(user, club_id):
    if not check_officer(user, club_id):
        print("Must be an officer to update club info.")
        return
    name = input("New name (leave blank to keep): ").strip() or None
    if get_club_by_name(name):
        print("Club already exists.")
        return None
    description = input("New description (leave blank to keep): ").strip() or None
    status = input("New activity status (leave blank to keep): ").strip() or None
    rec = update_club_info(club_id, name, description, status)
    if rec:
        print("Updated club:", rec["club_id"], rec["name"])
    else:
        print("No changes made.")

#officer tool - allow officers to mark members' dues as paid or unpaid
# ***works***
def manage_dues(user, club_id):
    if not check_officer(user, club_id):
        print("Must be an officer to manage dues.")
        return
    
    club = get_club_by_id(club_id)
    
    print(f"\n=== Manage Dues - {club['name']} ===")
    
    rows = list_memberships(club_id)
    if not rows:
        print("No members found.")
        return
    
    print("\nCurrent Members:")
    for i, r in enumerate(rows, 1):
        dues_status = "✅ Paid" if r.get('dues_paid') else "❌ Unpaid"
        print(f"{i}. {r.get('first_name')} {r.get('last_name')} - {r['role']} - Dues: {dues_status}")
    
    try:
        choice = int(input("\nSelect member number to toggle dues status (0 to cancel): ").strip())
        if choice == 0:
            return
        
        if 1 <= choice <= len(rows):
            member = rows[choice-1]
            user_id = member['userid']
            current_status = member.get('dues_paid', False)
            
            if current_status:
                if confirm_action(f"Mark {member.get('first_name')}'s dues as UNPAID?"):
                    rec = mark_dues_unpaid(club_id, user_id)
                    if rec:
                        print(f"✅ Dues marked as UNPAID for {member.get('first_name')}")
            else:
                if confirm_action(f"Mark {member.get('first_name')}'s dues as PAID?"):
                    rec = mark_dues_paid(club_id, user_id)
                    if rec:
                        print(f"✅ Dues marked as PAID for {member.get('first_name')}")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Please enter a valid number.")