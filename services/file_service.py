from models.file_resource import add_file, list_files_for_club
from models.events import list_events_for_club
from services.club_service import check_officer

def upload_file(current_user, club_id):
    if not check_officer(current_user, club_id):
        print("Only officers can upload files.")
        return

    url = input("Source URL: ").strip()
    event_choice = input("Associate with event? (y/n): ").strip().lower()
    event_id = None

    if event_choice == "y":
        events = list_events_for_club(club_id)
        if not events:
            print("No events for this club.")
        else:
            for e in events:
                print(f"{e['event_id']}: {e['name']}")
            event_id = int(input("Event ID: ").strip())

    record = add_file(club_id, url, event_id)
    print("File resource added:", record["file_id"])

def list_files(club_id):
    rows = list_files_for_club(club_id)
    if not rows:
        print("No files uploaded.")
        return
    for f in rows:
        print(f"[{f['file_id']}] {f['source_url']} (event_id={f['event_id']})")
