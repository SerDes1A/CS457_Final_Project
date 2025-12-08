from models.events import create_event, list_events_for_club, get_event
from models.club_membership import get_membership
from config import OFFICER_ROLES
from display import display_table
from input_validation import get_integer_input
from datetime import datetime

def check_officer(user, club_id):
    m = get_membership(club_id, user["user_id"])
    return bool(m and m["is_active"] and m["role"] in OFFICER_ROLES)

def event_creation(user):
    club_id = int(input("Club ID: ").strip())
    if not check_officer(user, club_id):
        print("Only officers can create events.")
        return
    name = input("Event name: ").strip()
    desc = input("Description: ").strip() or None
    start = input("Start (YYYY-MM-DD HH:MM, optional): ").strip() or None
    end = input("End (YYYY-MM-DD HH:MM, optional): ").strip() or None
    loc = input("Location: ").strip() or None
    ev = create_event(club_id, name, desc, start, end, loc)
    print("Created event:", ev["event_id"])

def list_events():
    club_id = (int(input("Club ID: ")).strip())
    rows = list_events_for_club(club_id)
    for r in rows:
        print(f"{r['event_id']:4} | {r['name']} | {r.get('start_datetime')}")

def view_event_details():
    """View detailed information about an event"""
    print("\n=== View Event Details ===")
    
    event_id = get_integer_input("Event ID: ", min_val=1)
    
    event = get_event(event_id)
    if not event:
        print("Event not found.")
        return
    
    # Get club name
    from models.clubs import get_club_by_id
    club = get_club_by_id(event['club'])
    club_name = club['name'] if club else f"Club ID: {event['club']}"
    print(f"\n📅 EVENT DETAILS")
    print("=" * 50)
    print(f"Event: {event['name']}")
    print(f"Club: {club_name}")
    print(f"Description: {event.get('description', 'No description')}")
    
    if event['start_datetime']:
        start_time = event['start_datetime'].strftime('%A, %B %d, %Y at %I:%M %p')
        print(f"Start: {start_time}")
    
    if event['end_datetime']:
        end_time = event['end_datetime'].strftime('%A, %B %d, %Y at %I:%M %p')
        print(f"End: {end_time}")
    
    print(f"Location: {event.get('location', 'TBD')}")
    print(f"Created: {event.get('created_at', 'Unknown')}")

def list_upcoming_events():
    """List upcoming events for all clubs"""
    print("\n=== Upcoming Events ===")
    
    from db.db_queries import fetch_all
    events = fetch_all('''
        SELECT e.*, c.name as club_name
        FROM "Event" e
        JOIN "Club" c ON e.club = c.club_id
        WHERE e.start_datetime > NOW()
        ORDER BY e.start_datetime
        LIMIT 20
    ''')
    
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
            'Location': e.get('location', 'TBD')[:20]
        })
    
    display_table(display_data, ['ID', 'Event', 'Club', 'Date', 'Location'], "Upcoming Events")
    