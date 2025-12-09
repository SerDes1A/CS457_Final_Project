# main.py
from services.authentication import register_user, login_user
from services.club_service import(
    list_out_clubs, create_club_service, join_club_request,
    list_memberships_for_club, list_out_user_clubs,
    approve_membership_service, promote_member, remove_member, 
    update_club_info_service, check_officer, manage_dues
)
from services.event_service import event_creation, view_event_details_with_clubs, list_upcoming_events
from services.task_service import task_creation, view_my_tasks, assign_task_to_user, view_my_tasks, update_task_status_service, edit_task_service
from services.attendance_service import mark_attendance_for_event, list_attendance
from services.file_service import list_files, upload_file
from services.dashboard_service import user_dashboard  # New import
from db.db_queries import fetch_all as qfetch_all
from input_validation import get_integer_input  # New import

import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    clear_screen()
    print("╔" + "═" * 58 + "╗")
    print(f"║{title:^58}║")
    print("╚" + "═" * 58 + "╝")

def main_menu():
    print_header("CLUB MANAGEMENT SYSTEM")
    print("""
    1. Register New Account
    2. Login
    3. Browse Clubs
    4. Create Club (becomes President)
    5. Exit
    """)

def member_menu(current_user):
    name = current_user.get('first_name', current_user['school_email'])
    print_header(f"WELCOME, {name.upper()}")
    print("""
    1. My Dashboard
    2. Browse Clubs
    3. View Upcoming Events
    4. View Event Details
    5. Create New Club
    6. Request to Join Club
    7. View My Memberships
    8. View My Assigned Tasks
    9. Update Task Status
    10. Officer Tools
    11. Logout
    """)

def officer_menu(club_name):
    display_name = club_name[:30] + "..." if len(club_name) > 30 else club_name
    print_header(f"OFFICER TOOLS: {display_name.upper()}")
    print("""
    1. View Club Members
    2. Approve Memberships
    3. Change Member Roles
    4. Remove Members
    5. Update Club Info
    6. Create Event
    7. Create Task
    8. Assign Task
    9. View Files
    10. Upload File
    11. Mark Attendance
    12. View Attendance
    13. Manage Dues
    14. Update Task Status
    15. Edit Task
    16. Back to Main Menu
    """)

def main():
    current_user = None
    while True:
        if not current_user:
            main_menu()
            choice = input("\n> ").strip()
            
            if choice == "1":
                print_header("REGISTER NEW ACCOUNT")
                register_user()
                input("\nPress Enter to continue...")
                
            elif choice == "2": 
                print_header("LOGIN")
                current_user = login_user()
                if current_user:
                    input("\nPress Enter to continue...")
                    
            elif choice == "3":
                print_header("BROWSE CLUBS")
                list_out_clubs()
                input("\nPress Enter to continue...")
                
            elif choice == "4":
                print_header("CREATE CLUB")
                print("You must be logged in to create a club.\n")
                input("Press Enter to continue...")
                continue
                
            elif choice == "5":
                print_header("GOODBYE!")
                print("Thank you for using the Club Management System.")
                break
                
            else:
                print("\nInvalid option. Please try again.")
                input("Press Enter to continue...")
                
        else:  # User is logged in
            member_menu(current_user)
            choice = input("\n> ").strip()
            
            if choice == "1":  # My Dashboard
                user_dashboard(current_user["user_id"])
                input("\nPress Enter to continue...")
                
            elif choice == "2":  # Browse Clubs
                print_header("BROWSE CLUBS")
                list_out_clubs()
                input("\nPress Enter to continue...")
                
            elif choice == "3":  # View Upcoming Events
                print_header("UPCOMING EVENTS")
                list_upcoming_events()
                input("\nPress Enter to continue...")

            elif choice == "4":  # View Event Details
                print_header("VIEW EVENT DETAILS")
                view_event_details_with_clubs(current_user)
                input("\nPress Enter to continue...")

            elif choice == "5":  # Create Club
                print_header("CREATE NEW CLUB")
                club = create_club_service(current_user)
                if club:
                    input("\nPress Enter to continue...")
                    
            elif choice == "6":  # Request to Join Club
                print_header("REQUEST TO JOIN CLUB")
                join_club_request(current_user)
                input("\nPress Enter to continue...")
                
            elif choice == "7":  # View My Memberships
                print_header("MY CLUB MEMBERSHIPS")
                list_out_user_clubs(current_user)
                input("\nPress Enter to continue...")
                
            elif choice == "8":  # View My Assigned Tasks
                print_header("MY ASSIGNED TASKS")
                view_my_tasks(current_user["user_id"])
                input("\nPress Enter to continue...")

            elif choice == "9":  # Update Task Status
                print_header("UPDATE TASK STATUS")
                update_task_status_service(current_user)
                input("\nPress Enter to continue...")  

            elif choice == "10":  # Officer Tools
                print_header("OFFICER TOOLS")
                print("Enter the Club ID you want to manage as an officer.")
                print("(You must be an officer of the club)")

                list_out_user_clubs(current_user)
                
                try:
                    club_id = get_integer_input("\nClub ID: ", min_val=1)
                    
                    if not check_officer(current_user, club_id):
                        print("\n❌ You are not an active officer for that club.")
                        input("Press Enter to continue...")
                        continue
                    
                    # Get club name for display
                    from models.clubs import get_club_by_id
                    club = get_club_by_id(club_id)
                    club_name = club['name'] if club else f"Club ID: {club_id}"
                    
                    # Officer tools loop
                    while True:
                        officer_menu(club_name)
                        opt = input("\n> ").strip()
                        
                        if opt == "1":  # View Club Members
                            print_header(f"CLUB MEMBERS - {club_name}")
                            list_memberships_for_club(club_id)
                            input("\nPress Enter to continue...")
                            
                        elif opt == "2":  # Approve Memberships
                            print_header(f"APPROVE MEMBERSHIPS - {club_name}")
                            approve_membership_service(current_user, club_id)
                            input("\nPress Enter to continue...")
                            
                        elif opt == "3":  # Change Member Roles
                            print_header(f"CHANGE MEMBER ROLES - {club_name}")
                            promote_member(current_user, club_id)
                            input("\nPress Enter to continue...")

                        elif opt == "4":  # Remove Members
                            print_header(f"REMOVE MEMBERS - {club_name}")
                            remove_member(current_user, club_id)
                            input("\nPress Enter to continue...")
                            
                        elif opt == "5":  # Update Club Info
                            print_header(f"UPDATE CLUB INFO - {club_name}")
                            update_club_info_service(current_user, club_id)
                            input("\nPress Enter to continue...")
                            
                        elif opt == "6":  # Create Event
                            print_header(f"CREATE EVENT - {club_name}")
                            event_creation(club_id)
                            input("\nPress Enter to continue...")
                            
                        elif opt == "7":  # Create Task
                            print_header(f"CREATE TASK - {club_name}")
                            task_creation(club_id)
                            input("\nPress Enter to continue...")
                            
                        elif opt == "8":  # Assign Task
                            print_header(f"ASSIGN TASK - {club_name}")
                            assign_task_to_user(club_id)
                            input("\nPress Enter to continue...")
                            
                        elif opt == "9":  # View Files
                            print_header(f"CLUB FILES - {club_name}")
                            list_files(club_id)
                            input("\nPress Enter to continue...")
                            
                        elif opt == "10":  # Upload File
                            print_header(f"UPLOAD FILE - {club_name}")
                            upload_file(current_user, club_id)
                            input("\nPress Enter to continue...")
                            
                        elif opt == "11":  # Mark Attendance
                            print_header(f"MARK ATTENDANCE - {club_name}")
                            mark_attendance_for_event(club_id)
                            input("\nPress Enter to continue...")
                            
                        elif opt == "12":  # View Attendance
                            print_header(f"VIEW ATTENDANCE - {club_name}")
                            list_attendance(club_id)
                            input("\nPress Enter to continue...")

                        elif opt == "13":  # Manage Dues
                            print_header(f"MANAGE DUES - {club_name}")
                            manage_dues(current_user, club_id)
                            input("\nPress Enter to continue...")


                        elif opt == "14":  # Update Task Status
                            print_header(f"UPDATE TASK STATUS - {club_name}")
                            update_task_status_service(current_user)
                            input("\nPress Enter to continue...")

                        elif opt == "15":  # Edit Task
                            print_header(f"EDIT TASK - {club_name}")
                            edit_task_service(current_user)
                            input("\nPress Enter to continue...")

                        elif opt == "16":  # Back to Main Menu (update this number)
                            print("\nReturning to main menu...")
                            break
                                                                                  
                        else:
                            print("\nInvalid option. Please try again.")
                                                
                except ValueError:
                    print("\n❌ Please enter a valid Club ID (number).")
                    input("Press Enter to continue...")
                except Exception as e:
                    print(f"\n❌ Error: {e}")
                    input("Press Enter to continue...")
                    
            elif choice == "11":  # Logout
                print_header("LOGOUT")
                print(f"Goodbye, {current_user.get('first_name', current_user['school_email'])}!")
                current_user = None
                input("\nPress Enter to continue...")
                
            else:
                print("\nInvalid option. Please try again.")
                input("Press Enter to continue...")

if __name__ == "__main__":
    main()