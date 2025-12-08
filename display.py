def display_table(data, columns, title=None):
    if not data:
        print("No data to display.")
        return
    
    if title:
        print(f"\n{title}")
        print("=" * 60)
    
    col_widths = {}
    for col in columns:
        col_widths[col] = len(col)
        for row in data:
            if col in row and row[col] is not None:
                col_widths[col] = max(col_widths[col], len(str(row[col])))
        col_widths[col] = min(col_widths[col] + 2, 30)
    
    header = " | ".join([f"{col:<{col_widths[col]}}" for col in columns])
    print(header)
    print("-" * len(header))
    
    for row in data:
        row_display = []
        for col in columns:
            value = row.get(col, "")
            if value is None:
                value = ""
            row_display.append(f"{str(value):<{col_widths[col]}}")
        print(" | ".join(row_display))

def select_from_list(items, prompt="Select an option:", display_func=None):
    if not items:
        print("No items available.")
        return None
    
    print(f"\n{prompt}")
    print("-" * 40)
    
    for i, item in enumerate(items, 1):
        if display_func:
            print(f"{i}. {display_func(item)}")
        else:
            print(f"{i}. {item}")
    
    while True:
        try:
            choice = input(f"\nEnter choice (1-{len(items)}), or 0 to cancel: ").strip()
            if choice == "0":
                return None
            
            idx = int(choice) - 1
            if 0 <= idx < len(items):
                return items[idx]
            else:
                print(f"Please enter a number between 1 and {len(items)}")
        except ValueError:
            print("Please enter a valid number.")

def confirm_action(prompt="Are you sure?"):
    response = input(f"{prompt} (yes/no): ").strip().lower()
    return response in ['yes', 'y']

def format_name(user):
    first = user.get('first_name', '')
    last = user.get('last_name', '')
    email = user.get('school_email', '')
    
    if first and last:
        return f"{first} {last} ({email})"
    elif email:
        return email
    else:
        return f"User ID: {user.get('user_id', 'N/A')}"

def format_club(club):
    name = club.get('name', 'Unknown')
    status = club.get('activity_status', '')
    club_id = club.get('club_id', '')
    
    if status:
        return f"{name} [{status}] (ID: {club_id})"
    return f"{name} (ID: {club_id})"

def display_selectable_list(items, title=None, item_formatter=None):
    """Display items with numbers for selection"""
    if not items:
        print("No items available.")
        return []
    
    if title:
        print(f"\n{title}")
        print("=" * 60)
    
    for i, item in enumerate(items, 1):
        if item_formatter:
            print(f"{i:3}. {item_formatter(item)}")
        else:
            print(f"{i:3}. {item}")
    
    return items

def get_selection_from_list(items, prompt="Enter your choice", allow_cancel=True):
    """Get user selection from a numbered list"""
    if not items:
        return None
    
    while True:
        try:
            if allow_cancel:
                choice_input = input(f"\n{prompt} (1-{len(items)}, 0 to cancel): ").strip()
            else:
                choice_input = input(f"\n{prompt} (1-{len(items)}): ").strip()
            
            if not choice_input:
                continue
                
            choice = int(choice_input)
            
            if choice == 0 and allow_cancel:
                return None
            
            if 1 <= choice <= len(items):
                return items[choice - 1]
            else:
                print(f"Please enter a number between 1 and {len(items)}")
                
        except ValueError:
            print("Please enter a valid number.")

def format_task_for_display(task):
    """Format task for display in selection list"""
    due_date = task['due_date'].strftime('%b %d, %Y') if task.get('due_date') else "No due date"
    priority_icon = {
        'High': '🔴',
        'Medium': '🟡', 
        'Low': '🟢'
    }.get(task.get('priority', 'Medium'), '⚪')
    
    status_icon = {
        'Not Started': '⏸️',
        'In Progress': '🔄',
        'Complete': '✅'
    }.get(task.get('status', 'Not Started'), '❓')
    
    return f"{priority_icon} {status_icon} {task['title']:30} | Due: {due_date:15} | Priority: {task.get('priority', 'N/A'):7}"

def format_event_for_display(event):
    """Format event for display in selection list"""
    if event.get('start_datetime'):
        start_time = event['start_datetime'].strftime('%b %d, %Y %I:%M %p')
    else:
        start_time = "Date TBD"
    
    location = event.get('location', 'Location TBD')[:20]
    
    return f"📅 {event['name']:30} | {start_time:25} | {location}"