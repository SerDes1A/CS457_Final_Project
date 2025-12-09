from models.file_resource import add_file, list_files_for_club
from services.club_service import check_officer

#officer tool - allow user to add a file URL attributed to the club
#***works***
def upload_file(current_user, club_id):
    if not check_officer(current_user, club_id):
        print("Only officers can upload files.")
        return

    while(1):
        name = input("Name for file (0 to cancel): ").strip()
        if name == 0:
            return
        elif name == "":
            ("Please have a name for the file.")
        else:
            break
    
    while(1):
        url = input("Source URL: ").strip()
        if url == "":
            ("Please input a URL.")
        else: break

    record = add_file(club_id, url, name)
    print("File resource added:", record["file_id"])

#officer tool - allow user to list out files that have been added
#***works***
def list_files(club_id):
    rows = list_files_for_club(club_id)
    if not rows:
        print("No files uploaded.")
        return
    for f in rows:
        print(f"\n[{f['name']}]")
        print(f"{f['source_url']}")
