from models.tasks import create_task, list_tasks
from models.task_assignment import assign_task
from models.club_membership import get_membership
from config import OFFICER_ROLES

def check_officer(user, club_id):
    m = get_membership(club_id, user["user_id"])
    return bool(m and m["is_active"] and m["role"] in OFFICER_ROLES)

def task_creation(user):
    club_id = int(input("Club ID: ").strip())
    if not check_officer(user, club_id):
        print("Only officers can create tasks.")
        return
    title = input("Title: ").strip()
    description = input("Description: ").strip() or None
    due_date = input("Due date (YYYY-MM-DD, optional): ").strip() or None
    priority = input("Priority (low/medium/high): ").strip() or None
    t = create_task(club_id, title, description, due_date, priority)
    print("Created Task:", t["task_id"], t["title"])

def list_club_tasks():
    club_id = int(input("Club ID: ").strip())
    rows = list_club_tasks(club_id)
    for r in rows:
        print(f"{r['task_id']:4} | {r['title']} | due: {r.get('due_date')} | status: {r.get('status')}")

def assign_task(user):
    task_id = int(input("Task ID: ").strip())
    user_id = int(input("User ID to assign to: ").strip())
    assign = assign_task(task_id, user_id)
    print("Assigned:", assign["assignment_id"])