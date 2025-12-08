# setup_test_data.py
from db.db_queries import execute, fetch_one, fetch_all
from services.authentication import hash_password
import sys

def create_test_users():
    """Create test users with different roles"""
    test_users = [
        {
            "email": "president@unr.edu",
            "password": "pres123",
            "first_name": "Alex",
            "last_name": "President",
            "role": "student"
        },
        {
            "email": "officer@unr.edu", 
            "password": "officer123",
            "first_name": "Jamie",
            "last_name": "Officer",
            "role": "student"
        },
        {
            "email": "member@unr.edu",
            "password": "member123", 
            "first_name": "Taylor",
            "last_name": "Member",
            "role": "student"
        },
        {
            "email": "regular@unr.edu",
            "password": "regular123",
            "first_name": "Casey",
            "last_name": "Regular",
            "role": "student"
        }
    ]
    
    print("Creating test users...")
    created_users = []
    
    for user_data in test_users:
        # Check if user exists
        existing = fetch_one('SELECT user_id FROM "User" WHERE school_email = %s', (user_data["email"],))
        if existing:
            print(f"  User already exists: {user_data['email']}")
            created_users.append(existing)
            continue
        
        # Create user
        hashed_pwd = hash_password(user_data["password"])
        sql = '''
        INSERT INTO "User" (school_email, password, first_name, last_name, role, created_at)
        VALUES (%s, %s, %s, %s, %s, NOW())
        RETURNING user_id, school_email, first_name, last_name;
        '''
        
        result = execute(sql, (
            user_data["email"],
            hashed_pwd,
            user_data["first_name"],
            user_data["last_name"],
            user_data["role"]
        ), returning=True)
        
        if result:
            created_users.append(result)
            print(f"  Created: {result['first_name']} {result['last_name']} ({result['school_email']})")
    
    return created_users

def get_club_id_by_name(club_name):
    """Get club ID by name"""
    result = fetch_one('SELECT club_id FROM "Club" WHERE name = %s', (club_name,))
    return result["club_id"] if result else None

def setup_club_memberships():
    """Set up club memberships with different roles"""
    print("\nSetting up club memberships...")
    
    # Get a club (use first one found)
    clubs = fetch_all('SELECT club_id, name FROM "Club" ORDER BY club_id LIMIT 3')
    if not clubs:
        print("No clubs found! Run the scraper first or create a test club.")
        return []
    
    # Get test users
    users = fetch_all('SELECT user_id, school_email, first_name, last_name FROM "User" WHERE school_email LIKE %s', ('%@unr.edu',))
    
    if len(users) < 4:
        print("Need at least 4 test users. Creating them now...")
        users_data = create_test_users()
        users = fetch_all('SELECT user_id, school_email, first_name, last_name FROM "User" WHERE school_email LIKE %s', ('%@unr.edu',))
    
    # Assign roles to first club
    club = clubs[0]
    print(f"\nSetting up roles for club: {club['name']} (ID: {club['club_id']})")
    
    roles = [
        ("president@unr.edu", "president"),
        ("officer@unr.edu", "officer"),
        ("member@unr.edu", "member"),
        ("regular@unr.edu", "member")  # Regular member, not in club
    ]
    
    memberships = []
    for email, role in roles:
        # Find user
        user = next((u for u in users if u["school_email"] == email), None)
        if not user:
            print(f"  User not found: {email}")
            continue
        
        # Check if membership exists
        existing = fetch_one('''
            SELECT membership_id FROM "Club Membership" 
            WHERE clubid = %s AND userid = %s
        ''', (club["club_id"], user["user_id"]))
        
        if existing:
            print(f"  Membership exists: {user['first_name']} as {role}")
            continue
        
        # Create membership
        sql = '''
        INSERT INTO "Club Membership" (clubid, userid, role, is_active, dues_paid)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING membership_id;
        '''
        
        # President and officer are active, regular member is not in this club
        is_active = role in ["president", "officer", "member"]
        
        result = execute(sql, (
            club["club_id"],
            user["user_id"],
            role,
            is_active,
            False  # dues_paid
        ), returning=True)
        
        if result:
            memberships.append({
                "user": user["first_name"] + " " + user["last_name"],
                "role": role,
                "active": is_active
            })
            print(f"  Added: {user['first_name']} as {role} ({'active' if is_active else 'not in club'})")
    
    return memberships

def create_test_events(club_id):
    """Create test events for a club"""
    print(f"\nCreating test events for club ID {club_id}...")
    
    test_events = [
        {
            "name": "Weekly Meeting",
            "description": "Regular weekly club meeting",
            "start_datetime": "2024-12-10 18:00:00",
            "end_datetime": "2024-12-10 19:30:00",
            "location": "Engineering Building Room 101"
        },
        {
            "name": "Project Workshop",
            "description": "Hands-on project building session",
            "start_datetime": "2024-12-15 14:00:00",
            "end_datetime": "2024-12-15 17:00:00",
            "location": "Maker Space"
        }
    ]
    
    for event in test_events:
        sql = '''
        INSERT INTO "Event" (club, name, description, start_datetime, end_datetime, location, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, NOW())
        RETURNING event_id, name;
        '''
        
        result = execute(sql, (
            club_id,
            event["name"],
            event["description"],
            event["start_datetime"],
            event["end_datetime"],
            event["location"]
        ), returning=True)
        
        if result:
            print(f"  Created event: {result['name']} (ID: {result['event_id']})")

def create_test_tasks(club_id):
    """Create test tasks for a club"""
    print(f"\nCreating test tasks for club ID {club_id}...")
    
    test_tasks = [
        {
            "title": "Prepare meeting agenda",
            "description": "Create agenda for next week's meeting",
            "due_date": "2024-12-08",
            "priority": "Medium"
        },
        {
            "title": "Order supplies",
            "description": "Order materials for project workshop",
            "due_date": "2024-12-12",
            "priority": "High"
        }
    ]
    
    for task in test_tasks:
        sql = '''
        INSERT INTO "Task" (club, title, description, due_date, created_at, updated_at, priority, status)
        VALUES (%s, %s, %s, %s, NOW(), NOW(), %s, 'Not Started')
        RETURNING task_id, title;
        '''
        
        result = execute(sql, (
            club_id,
            task["title"],
            task["description"],
            task["due_date"],
            task["priority"]
        ), returning=True)
        
        if result:
            print(f"  Created task: {result['title']} (ID: {result['task_id']})")

def display_test_scenario():
    """Display the test scenario for users"""
    print("\n" + "="*60)
    print("TEST SCENARIO SETUP")
    print("="*60)
    
    print("\n👥 TEST USERS (all passwords are '123' appended to role):")
    print("  President:   president@unr.edu / pres123")
    print("  Officer:     officer@unr.edu   / officer123")
    print("  Member:      member@unr.edu    / member123")
    print("  Regular:     regular@unr.edu   / regular123 (not in club)")
    
    print("\n🎯 CLUB ROLES (for first club in database):")
    print("  President:   Active, can do everything")
    print("  Officer:     Active, can manage members/events/tasks")
    print("  Member:      Active member, can view and attend")
    print("  Regular:     Not in club, must request to join")
    
    print("\n📝 WHAT TO TEST:")
    print("  1. Login as 'regular@unr.edu' and request to join club")
    print("  2. Login as 'president@unr.edu' and approve the request")
    print("  3. Login as 'officer@unr.edu' and create events/tasks")
    print("  4. Login as 'member@unr.edu' and view events, mark attendance")
    print("\n" + "="*60)

def main():
    """Main setup function"""
    print("Setting up test data for Club Management System...")
    
    # 1. Create test users
    users = create_test_users()
    
    # 2. Setup club memberships (need at least one club)
    clubs = fetch_all('SELECT club_id FROM "Club" LIMIT 1')
    if not clubs:
        print("\nNo clubs found! Please run the scraper first.")
        print("Or create a test club manually.")
        return
    
    memberships = setup_club_memberships()
    
    # 3. Create test events and tasks
    club_id = clubs[0]["club_id"]
    create_test_events(club_id)
    create_test_tasks(club_id)
    
    # 4. Display test scenario
    display_test_scenario()
    
    print("\n✅ Test data setup complete!")
    print("\nRun 'python main.py' to start testing.")

if __name__ == "__main__":
    main()