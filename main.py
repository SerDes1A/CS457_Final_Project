from db.connection import Database
from services.authentication import register_user, login_user
from services.club_service import(
    list_out_clubs, create_club, join_club_request,
    list_memberships_for_club, get_pending_requests,
    approve_membership, promote_member, remove_member, 
    update_club_info, check_officer
)
from services.event_service import event_creation, list_events
from services.task_service import task_creation, list_club_tasks, assign_task
from services.attendance_service import mark_attendance_for_event, list_attendance
from services.file_service import list_files, upload_file

def main_menu():
    print("""
          === Club Manager ===
          1. Register
          2. Login
          3. List Clubs
          4. Create Club 
          5. Exit
          """)
    
def member_menu():
    print("""
          Member Menu:
          1. List My Clubs
          2. Request to Join a Club
          3. List Events for a Club
          4. List Tasks for a Club
          5. List Files
          6. Logout
          """)

def officer_menu():
    print("""
          Officer Tools (Choose Club by Entering Club ID):
          1. List Club Members
          2. List Pending Membership Requests
          3. Approve Membership
          4. Promote/Demote Member
          5. Remove Member
          6. Update Club Info
          7. Create Event
          8. Create Task
          9. Assign Task
          10. List Files
          11. Upload Files
          12. Mark Attendance
          13. List Attendance
          14. Back to Main
          """)

def main():
    db = Database("localhost", "CS457_HW", "postgres", "D@t@_1")

    current_user = None
    while True:
        if not current_user:
            main_menu()
            choice = input("> ").strip()
            if choice == "1":
                register_user()
            elif choice == "2": 
                current_user = login_user()
            elif choice == "3":
                list_out_clubs()
            elif choice == "4":
                print("You must be logged in to create a club.")
                continue
            elif choice == "5":
                print("Goodbye.")
                break
            else:
                print("Invalid option.")
        else:
            print(f"\nLogged in as: {current_user.get('first_name') or current_user['school_email']}")
            print("""
                  1. List Clubs
                  2. Create a Club (you will be assigned president)
                  3. Request to Join a Club
                  4. My Memberships
                  5. Officer Tools
                  6. Logout
                  """)
            choice = input("> ").strip()
            if choice == "1": 
                list_out_clubs()
            elif choice == "2":
                create_club(current_user)
            elif choice == "3":
                join_club_request(current_user)
            elif choice == "4":
                from models.club_membership import fetch_one, fetch_all, list_memberships
                from db.db_queries import fetch_all as qfetch_all
                rows = qfetch_all("""
                                SELECT cm.*, c.name 
                                FROM "Club Membership" cm JOIN "Clubs" c ON cm.club_id = c.club_id
                                WhERE cm.user_id = %s;
                                """, (current_user["user_id"],))
                for r in rows:
                    status = "active" if r["is_active"] else "pending"
                    print(f"{r['club_id']:4} | {r['name']} | role: {r['role']} | {status}")
            elif choice == "5":
                club_id = int(input("Enter Club ID to manage as officer: ").strip())
                if not check_officer(current_user, club_id):
                    print("You are not an active officer for that club.")
                    continue
                while True:
                    officer_menu()
                    opt = input("> ").strip()
                    if opt == "1":
                        list_memberships_for_club(club_id)
                    elif opt == "2":
                        get_pending_requests(current_user, club_id)
                    elif opt == "3":
                        approve_membership(current_user, club_id)
                    elif opt == "4":
                        promote_member(current_user, club_id)
                    elif opt == "5":
                        remove_member(current_user, club_id)
                    elif opt == "6":
                        update_club_info(current_user, club_id)
                    elif opt == "7":
                        event_creation(current_user)
                    elif opt == "8":
                        task_creation(current_user)
                    elif opt == "9":
                        assign_task(current_user)
                    elif opt == "10":
                        list_files(club_id)
                    elif opt == "11":
                        upload_file(current_user, club_id)
                    elif opt == "12":
                        mark_attendance_for_event()
                    elif opt == "13":
                        list_attendance()
                    elif opt == "14":
                        break
                    else:
                        print("Invalid option.")
            elif choice == "6":
                current_user = None
            else: 
                print("Invalid option.")

if __name__ == "__main__":
    main()
