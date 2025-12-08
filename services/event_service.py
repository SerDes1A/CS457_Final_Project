from models.events import create_event, list_events_for_club
from models.club_membership import get_membership
from config import OFFICER_ROLES

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