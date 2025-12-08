from db.db_queries import fetch_all, fetch_one
from display import display_table

def user_dashboard(user_id):
    print("\n" + "="*60)
    print("MY DASHBOARD")
    print("="*60)
    

    user = fetch_one('SELECT * FROM "User" WHERE user_id = %s', (user_id,))
    if user:
        print(f"\n👤 User: {user['first_name']} {user['last_name']}")
        print(f"   Email: {user['school_email']}")
        print(f"   Role: {user['role'].title()}")
    
    memberships = fetch_all("""
        SELECT cm.*, c.name as club_name
        FROM "Club Membership" cm
        JOIN "Club" c ON cm.clubid = c.club_id
        WHERE cm.userid = %s
        ORDER BY c.name
    """, (user_id,))
    
    if memberships:
        print(f"\n🏢 Club Memberships ({len(memberships)}):")
        
        display_data = []
        for m in memberships:
            status = "✅ Active" if m['is_active'] else "⏳ Pending"
            role_display = m['role'].title() if m['role'] else "Member"
            
            display_data.append({
                'Club': m['club_name'],
                'Role': role_display,
                'Status': status,
                'Dues': "✅ Paid" if m.get('dues_paid') else "❌ Unpaid"
            })
        
        display_table(display_data, ['Club', 'Role', 'Status', 'Dues'])
    else:
        print("\n📭 You are not a member of any clubs yet.")
    
    events = fetch_all("""
        SELECT e.*, c.name as club_name
        FROM "Event" e
        JOIN "Club" c ON e.club = c.club_id
        JOIN "Club Membership" cm ON c.club_id = cm.clubid
        WHERE cm.userid = %s AND cm.is_active = true AND e.start_datetime > NOW()
        ORDER BY e.start_datetime
        LIMIT 5
    """, (user_id,))
    
    if events:
        print(f"\n📅 Upcoming Events ({len(events)}):")
        
        display_data = []
        for e in events:
            from datetime import datetime
            if e['start_datetime']:
                date_str = e['start_datetime'].strftime('%b %d, %Y %I:%M %p')
            else:
                date_str = "TBD"
            
            display_data.append({
                'Event': e['name'],
                'Club': e['club_name'],
                'Date': date_str,
                'Location': e.get('location', 'TBD')[:20]
            })
        
        display_table(display_data, ['Event', 'Club', 'Date', 'Location'])
    
    tasks = fetch_all("""
        SELECT t.*, c.name as club_name
        FROM "Task" t
        JOIN "Club" c ON t.club = c.club_id
        JOIN "Task Assignment" ta ON t.task_id = ta.task
        WHERE ta."user" = %s AND t.status != 'Complete'
        ORDER BY t.due_date
        LIMIT 5
    """, (user_id,))
    
    if tasks:
        print(f"\n📋 Your Tasks ({len(tasks)}):")
        
        display_data = []
        for t in tasks:
            due_date = t['due_date'].strftime('%b %d, %Y') if t['due_date'] else "No due date"
            
            display_data.append({
                'Task': t['title'],
                'Club': t['club_name'],
                'Due': due_date,
                'Priority': t['priority'],
                'Status': t['status']
            })
        
        display_table(display_data, ['Task', 'Club', 'Due', 'Priority', 'Status'])
    
    print("\n" + "="*60)