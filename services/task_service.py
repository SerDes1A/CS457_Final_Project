from db.db_queries import fetch_all
from models.tasks import create_task, list_tasks, update_task, update_task_status, get_task
from models.task_assignment import assign_task
from models.club_membership import get_membership
from models.clubs import get_club_by_id
from input_validation import get_integer_input, confirm_action
from display import display_table
from config import OFFICER_ROLES

def check_officer(user, club_id):
    m = get_membership(club_id, user["user_id"])
    return bool(m and m["is_active"] and m["role"] in OFFICER_ROLES)

def task_creation(user):
    print("\n=== Create New Task ===")
    
    officer_clubs = fetch_all('''
        SELECT c.club_id, c.name 
        FROM "Club" c
        JOIN "Club Membership" cm ON c.club_id = cm.clubid
        WHERE cm.userid = %s 
          AND cm.is_active = true 
          AND cm.role IN ('president', 'officer', 'treasurer', 'secretary')
        ORDER BY c.name
    ''', (user["user_id"],))
    
    if not check_officer:
        print("You are not an officer of any clubs. Only officers can create tasks.")
        return
    
    print("\nYour Clubs (Officer Access):")
    print("-" * 50)
    for i, club in enumerate(officer_clubs, 1):
        print(f"{i}. {club['name']} (ID: {club['club_id']})")
    
    try:
        choice = int(input(f"\nSelect club (1-{len(officer_clubs)}): ").strip())
        if 1 <= choice <= len(officer_clubs):
            club = officer_clubs[choice-1]
            club_id = club['club_id']
        else:
            print("Invalid selection.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return
    
    print(f"\nCreating task for: {club['name']}")
    
    title = input("Task title: ").strip()
    if not title:
        print("Task title is required.")
        return
    
    description = input("Description (optional): ").strip() or None
  
    while True:
        due_date = input("Due date (YYYY-MM-DD, required): ").strip()
        if due_date:
            if len(due_date) == 10 and due_date[4] == '-' and due_date[7] == '-':
                break
            else:
                print("Please use YYYY-MM-DD format.")
        else:
            print("Due date is required!")
    
    print("\nPriority:")
    print("1. Low")
    print("2. Medium (default)")
    print("3. High")
    
    priority_choice = input("Select priority (1-3): ").strip()
    priority_map = {'1': 'Low', '2': 'Medium', '3': 'High'}
    priority = priority_map.get(priority_choice, 'Medium')
    
    print(f"\nTask Summary:")
    print(f"  Club: {club['name']}")
    print(f"  Title: {title}")
    if description:
        print(f"  Description: {description[:50]}...")
    print(f"  Due Date: {due_date}")
    print(f"  Priority: {priority}")
    
    confirm = input("\nCreate this task? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("Task creation cancelled.")
        return
    
    try:
        t = create_task(club_id, title, description, due_date, priority)
        print(f"\n✅ Task '{t['title']}' created successfully!")
        print(f"   Task ID: {t['task_id']}")
    except Exception as e:
        print(f"❌ Error creating task: {e}")

def list_club_tasks():
    club_id = int(input("Club ID: ").strip())
    rows = list_tasks(club_id)
    for r in rows:
        print(f"{r['task_id']:4} | {r['title']} | due: {r.get('due_date')} | status: {r.get('status')}")

def assign_task(user):
    task_id = int(input("Task ID: ").strip())
    user_id = int(input("User ID to assign to: ").strip())
    assign = assign_task(task_id, user_id)
    print("Assigned:", assign["assignment_id"])

def update_task_status_service(user):
    """Update status of a task"""
    print("\n=== Update Task Status ===")
    
    task_id = get_integer_input("Task ID: ", min_val=1)
    task = get_task(task_id)
    if not task:
        print("Task not found.")
        return
    
    if not check_officer(user, task['club']):
        print("Only officers can update task status.")
        return
    
    print(f"\nTask: {task['title']}")
    print(f"Current Status: {task['status']}")
    
    print("\nNew Status Options:")
    print("1. Not Started")
    print("2. In Progress")
    print("3. Complete")
    
    status_map = {
        '1': 'Not Started',
        '2': 'In Progress',
        '3': 'Complete'
    }
    
    choice = input("\nSelect new status (1-3): ").strip()
    if choice not in status_map:
        print("Invalid choice.")
        return
    
    new_status = status_map[choice]
    
    if confirm_action(f"Change task status to '{new_status}'?"):
        try:
            updated = update_task_status(task_id, new_status)
            print(f"✅ Task status updated to: {updated['status']}")
        except Exception as e:
            print(f"❌ Error: {e}")

def edit_task_service(user):
    print("\n=== Edit Task ===")
    
    task_id = get_integer_input("Task ID: ", min_val=1)
    
    task = get_task(task_id)
    if not task:
        print("Task not found.")
        return
    
    if not check_officer(user, task['club']):
        print("Only officers can edit tasks.")
        return
    
    print(f"\nCurrent Task: {task['title']}")
    print(f"Description: {task.get('description', 'None')}")
    print(f"Due Date: {task.get('due_date', 'None')}")
    print(f"Priority: {task.get('priority', 'None')}")
    
    print("\nEnter new values (leave blank to keep current):")
    
    title = input(f"Title [{task['title']}]: ").strip()
    if not title:
        title = None
    
    description = input(f"Description [{task.get('description', '')}]: ").strip()
    if not description:
        description = None
    
    due_date = input(f"Due Date (YYYY-MM-DD) [{task.get('due_date', '')}]: ").strip()
    if not due_date:
        due_date = None
    
    priority_input = input(f"Priority (low/medium/high) [{task.get('priority', '')}]: ").strip().lower()
    priority_map = {'low': 'Low', 'medium': 'Medium', 'high': 'High', 'l': 'Low', 'm': 'Medium', 'h': 'High'}
    priority = priority_map.get(priority_input) if priority_input else None
    
    if any([title, description, due_date, priority]):
        if confirm_action("Update task with these changes?"):
            try:
                updated = update_task(task_id, title, description, due_date, priority)
                print(f"✅ Task updated: {updated['title']}")
            except Exception as e:
                print(f"❌ Error: {e}")
    else:
        print("No changes made.")

def view_my_tasks(user_id):
    tasks = fetch_all("""
        SELECT t.*, c.name as club_name
        FROM "Task" t
        JOIN "Club" c ON t.club = c.club_id
        JOIN "Task Assignment" ta ON t.task_id = ta.task
        WHERE ta."user" = %s
        ORDER BY t.due_date, t.priority
    """, (user_id,))
    
    if not tasks:
        print("\nYou have no assigned tasks.")
        return
    
    display_data = []
    for t in tasks:
        due_date = t['due_date'].strftime('%b %d, %Y') if t['due_date'] else "No due date"
        
        # Color code by priority
        priority_display = t['priority']
        if t['priority'] == 'High':
            priority_display = "🔴 " + priority_display
        elif t['priority'] == 'Medium':
            priority_display = "🟡 " + priority_display
        else:
            priority_display = "🟢 " + priority_display
        
        # Color code by status
        status_display = t['status']
        if t['status'] == 'Complete':
            status_display = "✅ " + status_display
        elif t['status'] == 'In Progress':
            status_display = "🔄 " + status_display
        else:
            status_display = "⏸️ " + status_display
        
        display_data.append({
            'Task ID': t['task_id'],
            'Title': t['title'],
            'Club': t['club_name'],
            'Due': due_date,
            'Priority': priority_display,
            'Status': status_display
        })
    
    display_table(display_data, ['Task ID', 'Title', 'Club', 'Due', 'Priority', 'Status'], "My Assigned Tasks")

def view_task_details():
    print("\n=== View Task Details ===")
    
    task_id = get_integer_input("Task ID: ", min_val=1)
    
    task = get_task(task_id)
    if not task:
        print("Task not found.")
        return
    
    club = get_club_by_id(task['club'])
    club_name = club['name'] if club else f"Club ID: {task['club']}"
    
    print(f"\n📋 TASK DETAILS")
    print("=" * 50)
    print(f"Task: {task['title']}")
    print(f"Club: {club_name}")
    print(f"Description: {task.get('description', 'No description')}")
    
    if task['due_date']:
        due_date = task['due_date'].strftime('%A, %B %d, %Y')
        print(f"Due Date: {due_date}")
    else:
        print("Due Date: Not set")
    
    print(f"Priority: {task.get('priority', 'Not set')}")
    print(f"Status: {task.get('status', 'Not Started')}")
    print(f"Created: {task.get('created_at', 'Unknown')}")
    print(f"Last Updated: {task.get('updated_at', 'Unknown')}")
    
    assignees = fetch_all('''
        SELECT u.user_id, u.first_name, u.last_name, u.school_email
        FROM "Task Assignment" ta
        JOIN "User" u ON ta."user" = u.user_id
        WHERE ta.task = %s
    ''', (task_id,))
    
    if assignees:
        print(f"\nAssigned to ({len(assignees)}):")
        for a in assignees:
            print(f"  • {a['first_name']} {a['last_name']} ({a['school_email']})")