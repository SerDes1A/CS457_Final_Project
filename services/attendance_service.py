from models.attendance import mark_attendance, list_event_attendance

def mark_attendance_for_event():
    event_id = int(input("Event ID: ").strip())
    user_id = int(input("User ID: ").strip())
    status = input("Status (attended/absent): ").strip() or "attended"
    rec = mark_attendance(event_id, user_id, status)
    print("recorded attendance:", rec["attendance_id"])

def list_attendance():
    event_id = int(input("Event ID: ").strip())
    rows = list_event_attendance(event_id)
    for r in rows:
        print(f"{r['user_id']:4} | {r.get('first_name')} {r.get('last_name')} | {r['status']}")