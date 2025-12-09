from models.attendance import mark_attendance, list_event_attendance
from models.events import list_events_for_club, get_event
from models.club_membership import list_memberships
from display import display_table

def mark_attendance_for_event(club_id):
    print("\n=== Mark Attendance ===")
    
    # First, list events for the club
    events = list_events_for_club(club_id)
    if not events:
        print("No events found for this club.")
        return
    
    print("\nAvailable Events:")
    print("-" * 40)
    for i, event in enumerate(events, 1):
        if event['start_datetime']:
            date_str = event['start_datetime'].strftime('%b %d, %Y %I:%M %p')
        else:
            date_str = "Date TBD"
        print(f"{i}. {event['name']} - {date_str} (ID: {event['event_id']})")
    
    try:
        event_choice = int(input(f"\nSelect event (1-{len(events)}): ").strip())
        if 1 <= event_choice <= len(events):
            event_id = events[event_choice-1]['event_id']
            event_name = events[event_choice-1]['name']
        else:
            print("Invalid selection.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return
    
    # Now list club members
    members = list_memberships(club_id)
    if not members:
        print("No members found for this club.")
        return
    
    # Filter only active members
    active_members = [m for m in members if m['is_active']]
    if not active_members:
        print("No active members found.")
        return
    
    print(f"\nActive Members for {event_name}:")
    print("-" * 50)
    for i, member in enumerate(active_members, 1):
        print(f"{i}. {member.get('first_name')} {member.get('last_name')} (ID: {member['userid']})")
    
    try:
        member_choice = int(input(f"\nSelect member (1-{len(active_members)}): ").strip())
        if 1 <= member_choice <= len(active_members):
            user_id = active_members[member_choice-1]['userid']
            user_name = f"{active_members[member_choice-1]['first_name']} {active_members[member_choice-1]['last_name']}"
        else:
            print("Invalid selection.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return
    
    print("\nStatus options: Present, Absent")
    status_input = input(f"Status for {user_name} (Present/Absent): ").strip() or "Present"
    
    # Mark attendance
    rec = mark_attendance(event_id, user_id, status_input)
    if rec:
        print(f"\n✅ Attendance recorded!")
        print(f"   Event: {event_name}")
        print(f"   Member: {user_name}")
        print(f"   Status: {rec['status']}")
        print(f"   Time: {rec['time']}")
    else:
        print("❌ Failed to record attendance.")

def list_attendance(club_id):
    print("\n=== View Event Attendance ===")
    
    # First, list events for the club
    events = list_events_for_club(club_id)
    if not events:
        print("No events found for this club.")
        return
    
    print("\nAvailable Events:")
    print("-" * 40)
    for i, event in enumerate(events, 1):
        if event['start_datetime']:
            date_str = event['start_datetime'].strftime('%b %d, %Y')
        else:
            date_str = "Date TBD"
        print(f"{i}. {event['name']} - {date_str} (ID: {event['event_id']})")
    
    try:
        event_choice = int(input(f"\nSelect event (1-{len(events)}): ").strip())
        if 1 <= event_choice <= len(events):
            event_id = events[event_choice-1]['event_id']
            event_name = events[event_choice-1]['name']
        else:
            print("Invalid selection.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return
    
    # Get attendance for the selected event
    rows = list_event_attendance(event_id)
    if not rows:
        print(f"\nNo attendance records found for '{event_name}'.")
        return
    
    # Prepare data for display
    display_data = []
    for r in rows:
        status_display = "✅ Present" if r['status'] == 'Present' else "❌ Absent"
        
        display_data.append({
            'User ID': r['user'],
            'Name': f"{r.get('first_name', '')} {r.get('last_name', '')}",
            'Status': status_display,
            'Time': r.get('time', '').strftime('%Y-%m-%d %H:%M') if r.get('time') else 'N/A'
        })
    
    print(f"\n📊 Attendance for '{event_name}'")
    display_table(display_data, ['User ID', 'Name', 'Status', 'Time'])