from db.db_queries import fetch_all, fetch_one
from models.tasks import create_task, list_tasks, update_task, update_task_status, get_task, get_task_by_club
from models.task_assignment import assign_task
from models.club_membership import get_membership, get_user_memberships
from models.clubs import get_club_by_id
from services.club_service import list_memberships_for_club
from input_validation import get_integer_input, confirm_action
from display import display_table
from config import OFFICER_ROLES

#check if user is officer
#***works***
def check_officer(user, club_id):
    m = get_membership(club_id, user["user_id"])
    return bool(m and m["is_active"] and m["role"] in OFFICER_ROLES)

#create new task for a club
#***works***
def task_creation(club_id):
    print("\n=== Create New Task ===")
    
    club = get_club_by_id(club_id)
    
    print(f"\nCreating task for: {club['name']}")
    
    title = input("Task title (0 to cancel): ").strip()
    if title == "0":
        return
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


def list_club_tasks(club_id):
    rows = list_tasks(club_id)
    for r in rows:
        print(f"{r['task_id']:4} | {r['title']} | due: {r.get('due_date')} | status: {r.get('status')}")

#officer tool - assign a task to a user
#***works***
def assign_task_to_user(club_id):
    print("\n=== Assign Task to User ===")
    list_club_tasks(club_id)
    while(1):
        task_id = int(input("Task ID (0 to cancel): ").strip())
        if task_id == 0:
            return
        if (not get_task_by_club(task_id, club_id)):
            print("Not a valid task.")
        else:
            break
    
    list_memberships_for_club(club_id)
    while(1):
        user_id = int(input("User ID to assign to: ").strip())
        if(not get_membership(club_id, user_id)):
            print("Invalid user ID")
        else:
            assign = assign_task(task_id, user_id)
            print("Assigned:", assign["assignment_id"])
            return

#allow for users to update a task
#for regular members, only update status of tasks assigned to them
#for officers, can update any task in the club
def update_task_status_service(user):
    print("\n=== Update Task Status ===")
    
    # First, show user's clubs
    from models.club_membership import get_user_memberships
    clubs = get_user_memberships(user['user_id'])
    active_clubs = [c for c in clubs if c['is_active']]
    
    if not active_clubs:
        print("You are not a member of any active clubs.")
        return
    
    print("\nYour Active Clubs:")
    print("-" * 50)
    for i, club in enumerate(active_clubs, 1):
        print(f"{i}. {club['name']} (Role: {club['role']})")
    
    try:
        club_choice = int(input(f"\nSelect club (1-{len(active_clubs)}): ").strip())
        if 1 <= club_choice <= len(active_clubs):
            selected_club = active_clubs[club_choice-1]
            club_id = selected_club['clubid']
            club_name = selected_club['name']
        else:
            print("Invalid selection.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return
    
    # Get tasks based on user role
    if check_officer(user, club_id):
        # Officer can see all club tasks
        tasks = list_tasks(club_id)
        print(f"\nAll Tasks for {club_name}:")
    else:
        # Regular member sees only their assigned tasks
        tasks = fetch_all("""
            SELECT t.*
            FROM "Task" t
            JOIN "Task Assignment" ta ON t.task_id = ta.task
            WHERE t.club = %s AND ta."user" = %s
            ORDER BY t.due_date
        """, (club_id, user['user_id']))
        print(f"\nYour Assigned Tasks for {club_name}:")
    
    if not tasks:
        print("No tasks found.")
        return
    
    # Display tasks
    for i, task in enumerate(tasks, 1):
        due_date = task['due_date'].strftime('%b %d, %Y') if task['due_date'] else "No due date"
        status_icon = "✅" if task['status'] == 'Complete' else "🔄" if task['status'] == 'In Progress' else "⏸️"
        print(f"{i}. {task['title']} - Due: {due_date} - Status: {status_icon} {task['status']} (ID: {task['task_id']})")
    
    try:
        task_choice = int(input(f"\nSelect task to update (1-{len(tasks)}): ").strip())
        if 1 <= task_choice <= len(tasks):
            task_id = tasks[task_choice-1]['task_id']
            task_title = tasks[task_choice-1]['title']
            current_status = tasks[task_choice-1]['status']
        else:
            print("Invalid selection.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return
    
    # Check if user is assigned to this task (for non-officers)
    if not check_officer(user, club_id):
        # Verify the task is assigned to the user
        assigned_task = fetch_one("""
            SELECT 1 FROM "Task Assignment"
            WHERE task = %s AND "user" = %s
        """, (task_id, user['user_id']))
        
        if not assigned_task:
            print("❌ You can only update tasks assigned to you.")
            return
    
    # Show current status and get new status
    print(f"\nTask: {task_title}")
    print(f"Current Status: {current_status}")
    
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
    
    if confirm_action(f"Change task status from '{current_status}' to '{new_status}'?"):
        try:
            updated = update_task_status(task_id, new_status)
            print(f"✅ Task status updated to: {updated['status']}")
        except Exception as e:
            print(f"❌ Error: {e}")

def edit_task_service(user):
    print("\n=== Edit Task ===")
    
    clubs = get_user_memberships(user['user_id'])
    officer_clubs = [c for c in clubs if c['is_active'] and check_officer(user, c['clubid'])]
    
    if not officer_clubs:
        print("You are not an officer of any active clubs.")
        return
    
    print("\nYour Clubs (Officer Role):")
    print("-" * 50)
    for i, club in enumerate(officer_clubs, 1):
        print(f"{i}. {club['name']} (Role: {club['role']})")
    
    try:
        club_choice = int(input(f"\nSelect club (1-{len(officer_clubs)}): ").strip())
        if 1 <= club_choice <= len(officer_clubs):
            selected_club = officer_clubs[club_choice-1]
            club_id = selected_club['clubid']
            club_name = selected_club['name']
        else:
            print("Invalid selection.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return
    
    tasks = list_tasks(club_id)
    if not tasks:
        print(f"No tasks found for {club_name}.")
        return
    
    print(f"\nTasks for {club_name}:")
    print("-" * 60)
    
    for i, task in enumerate(tasks, 1):
        due_date = task['due_date'].strftime('%b %d, %Y') if task['due_date'] else "No due date"
        status_icon = "✅" if task['status'] == 'Complete' else "🔄" if task['status'] == 'In Progress' else "⏸️"
        priority_icon = "🔴" if task['priority'] == 'High' else "🟡" if task['priority'] == 'Medium' else "🟢"

        description = task.get('description', '')
        if description and len(description) > 30:
            description = description[:27] + "..."
        
        print(f"{i}. {task['title']}")
        print(f"   ID: {task['task_id']} | Status: {status_icon} {task['status']}")
        print(f"   Due: {due_date} | Priority: {priority_icon} {task['priority']}")
        if description:
            print(f"   Description: {description}")
        print()

    try:
        task_choice = int(input(f"\nSelect task to edit (1-{len(tasks)}): ").strip())
        if 1 <= task_choice <= len(tasks):
            task_id = tasks[task_choice-1]['task_id']
            task = tasks[task_choice-1]  
        else:
            print("Invalid selection.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return
    
    print(f"\n📋 Current Task Details:")
    print("=" * 50)
    print(f"Title: {task['title']}")
    print(f"Description: {task.get('description', 'None')}")
    print(f"Due Date: {task.get('due_date', 'None')}")
    print(f"Priority: {task.get('priority', 'None')}")
    print(f"Status: {task.get('status', 'None')}")
    
    print("\n📝 Enter new values (leave blank to keep current):")
    print("-" * 50)
    
    # Get new values
    title = input(f"Title [{task['title']}]: ").strip()
    if not title:
        title = None
    
    description = input(f"Description [{task.get('description', '')}]: ").strip()
    if not description:
        description = None
    
    due_date = input(f"Due Date (YYYY-MM-DD) [{task.get('due_date', '')}]: ").strip()
    if not due_date:
        due_date = None

    while True:
        priority_input = input(f"Priority (low/medium/high) [{task.get('priority', '')}]: ").strip().lower()
        if not priority_input:
            priority = None
            break
        
        priority_map = {
            'low': 'Low', 'l': 'Low',
            'medium': 'Medium', 'med': 'Medium', 'm': 'Medium',
            'high': 'High', 'h': 'High'
        }
        
        if priority_input in priority_map:
            priority = priority_map[priority_input]
            break
        else:
            print("Invalid priority. Please enter 'low', 'medium', or 'high'.")

    print("\nWould you like to update the task status?")
    print("1. Not Started")
    print("2. In Progress")
    print("3. Complete")
    print("4. Keep current status")
    
    status_choice = input("\nSelect status option (1-4): ").strip()
    status_map = {
        '1': 'Not Started',
        '2': 'In Progress',
        '3': 'Complete',
        '4': None
    }
    
    if status_choice in status_map:
        new_status = status_map[status_choice]
    else:
        print("Invalid choice. Keeping current status.")
        new_status = None
 
    print(f"\n📋 Changes Summary:")
    print("=" * 50)
    changes = []
    
    if title and title != task['title']:
        changes.append(f"  Title: {task['title']} → {title}")
    if description and description != task.get('description'):
        changes.append(f"  Description: Updated")
    if due_date and str(due_date) != str(task.get('due_date')):
        changes.append(f"  Due Date: {task.get('due_date')} → {due_date}")
    if priority and priority != task.get('priority'):
        changes.append(f"  Priority: {task.get('priority')} → {priority}")
    if new_status and new_status != task.get('status'):
        changes.append(f"  Status: {task.get('status')} → {new_status}")
    
    if not any([title, description, due_date, priority, new_status]):
        print("No changes made.")
        return
    
    if changes:
        print("\nThe following changes will be made:")
        for change in changes:
            print(change)
    else:
        print("No changes detected (values are the same as current).")
        return
    
    if confirm_action("\nApply these changes to the task?"):
        try:
            updated = update_task(task_id, title, description, due_date, priority)
            if new_status:
                updated = update_task_status(task_id, new_status)
            
            print(f"\n✅ Task '{updated['title']}' updated successfully!")

            print(f"\n📋 Final Task State:")
            print("-" * 40)
            print(f"Title: {updated['title']}")
            print(f"Description: {updated.get('description', 'None')}")
            print(f"Due Date: {updated.get('due_date', 'None')}")
            print(f"Priority: {updated.get('priority', 'None')}")
            print(f"Status: {updated.get('status', 'None')}")
            
        except Exception as e:
            print(f"❌ Error updating task: {e}")

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