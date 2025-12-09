from models.events import create_event, list_events_for_club
from db.db_queries import fetch_all
from models.club_membership import get_membership
from models.clubs import get_club_by_id
from models.events import get_event
from config import OFFICER_ROLES
from display import display_table

#check if user is an officer
#***works***
def check_officer(user, club_id):
    m = get_membership(club_id, user["user_id"])
    return bool(m and m["is_active"] and m["role"] in OFFICER_ROLES)

#officer tools - create new event
#***works***
def event_creation(club_id):
    print("\n=== Create New Event ===")
    
    club = get_club_by_id(club_id)
    
    print(f"\nCreating event for: {club['name']}")
    print("-" * 40)
    
    while(1):
        name = input("Event name (0 to cancel): ").strip()
        if name == "0":
            return
        if not name:
            print("Event name is required.")
        else:
            break
    
    description = input("Description (optional): ").strip() or None
    
    print("\nEvent Dates/Times (use YYYY-MM-DD HH:MM format, 24-hour time)")
    print("Example: 2024-12-25 14:30")
    
    start_datetime = input("Start date/time: ").strip()
    if not start_datetime:
        print("Start date/time is required.")
        return
    
    end_datetime = input("End date/time (optional): ").strip() or None
    location = input("Location (optional): ").strip() or None
    
    print(f"\nEvent Summary:")
    print(f"  Club: {club['name']}")
    print(f"  Name: {name}")
    if description:
        print(f"  Description: {description[:50]}...")
    print(f"  Start: {start_datetime}")
    if end_datetime:
        print(f"  End: {end_datetime}")
    if location:
        print(f"  Location: {location}")
    
    confirm = input("\nCreate this event? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("Event creation cancelled.")
        return
    
    try:
        ev = create_event(club_id, name, description, start_datetime, end_datetime, location)
        print(f"\n✅ Event '{ev['name']}' created successfully!")
        print(f"   Event ID: {ev['event_id']}")
    except Exception as e:
        print(f"❌ Error creating event: {e}")

#list out events a club has
#***works**
def list_events(club_id):
    club = get_club_by_id(club_id)
    print(f"\nEvents for {club['name']}")
    print("-" * 40)
    rows = list_events_for_club(club)
    for r in rows:
        print(f"{r['event_id']:4} | {r['name']} | {r.get('start_datetime')}")

#list out upcoming events (events that are marked as later than what is at now())
#***works***
def list_upcoming_events():
    print("\n=== Upcoming Events ===")
    events = fetch_all("""
        SELECT e.*, c.name as club_name
        FROM "Event" e
        JOIN "Club" c ON e.club = c.club_id
        WHERE e.start_datetime > NOW()
        ORDER BY e.start_datetime
        LIMIT 20
        """)
    
    if not events:
        print("No upcoming events.")
        return
    
    display_data = []
    for e in events:
        start_time = e['start_datetime'].strftime('%b %d, %Y %I:%M %p') if e['start_datetime'] else "TBD"
        
        display_data.append({
            'ID': e['event_id'],
            'Event': e['name'],
            'Club': e['club_name'],
            'Date': start_time,
            'Location': (e.get('location') or 'TBD')[:20]
        })
    
    display_table(display_data, ['ID', 'Event', 'Club', 'Date', 'Location'], "Upcoming Events")

#list out all events with a club and get details
#***works***
def view_event_details_with_clubs(user):
    print("\n=== View Event Details ===")
    
    member_clubs = fetch_all('''
        SELECT c.club_id, c.name 
        FROM "Club" c
        JOIN "Club Membership" cm ON c.club_id = cm.clubid
        WHERE cm.userid = %s AND cm.is_active = true
        ORDER BY c.name
    ''', (user["user_id"],))
    
    if not member_clubs:
        print("You are not a member of any clubs.")
        return
    
    print("\nYour Clubs:")
    print("-" * 50)
    for i, club in enumerate(member_clubs, 1):
        print(f"{i}. {club['name']}")
    
    try:
        choice = int(input(f"\nSelect club (1-{len(member_clubs)}): ").strip())
        if 1 <= choice <= len(member_clubs):
            club = member_clubs[choice-1]
            club_id = club['club_id']
        else:
            print("Invalid selection.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    events = list_events_for_club(club_id)
    if not events:
        print(f"\nNo events found for {club['name']}.")
        return
    
    print(f"\nEvents for {club['name']}:")
    print("-" * 50)
    for i, event in enumerate(events, 1):
        if event['start_datetime']:
            date_str = event['start_datetime'].strftime('%b %d, %Y')
        else:
            date_str = "Date TBD"
        print(f"{i}. {event['name']} - {date_str} (ID: {event['event_id']})")
    
    try:
        event_choice = int(input(f"\nSelect event to view details (1-{len(events)}): ").strip())
        if 1 <= event_choice <= len(events):
            event = events[event_choice-1]
            event_id = event['event_id']
            print(f"\n📅 EVENT DETAILS")
            print("=" * 50)
            print(f"Event: {event['name']}")
            print(f"Club: {club['name']}")
            print(f"Description: {event.get('description', 'No description')}")
            
            if event['start_datetime']:
                start_time = event['start_datetime'].strftime('%A, %B %d, %Y at %I:%M %p')
                print(f"Start: {start_time}")
            
            if event['end_datetime']:
                end_time = event['end_datetime'].strftime('%A, %B %d, %Y at %I:%M %p')
                print(f"End: {end_time}")
            
            print(f"Location: {event.get('location', 'TBD')}")
            print(f"Created: {event.get('created_at', 'Unknown')}")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Please enter a valid number.")
    
#might add an option to modify event details so that get_event is used