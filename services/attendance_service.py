from models.attendance import mark_attendance, list_event_attendance

def mark_attendance_for_event():
    event_id = int(input("Event ID: ").strip())
    user_id = int(input("User ID: ").strip())
    print("Status options: Present, Absent")
    status_input = input("Status (Present/Absent): ").strip() or "Present"
    
    rec = mark_attendance(event_id, user_id, status_input)
    print("Recorded attendance:", rec["attendance_id"])

def list_attendance():
    event_id = int(input("Event ID: ").strip())
    rows = list_event_attendance(event_id)
    for r in rows:
        print(f"{r['user']:4} | {r.get('first_name')} {r.get('last_name')} | {r['status']}")