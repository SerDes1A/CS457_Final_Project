def display_table(data, columns, title=None):
    if not data:
        print("No data to display.")
        return
    
    if title:
        print(f"\n{title}")
        print("=" * 60)
    
    # Calculate column widths
    col_widths = {}
    for col in columns:
        # Start with column name width
        col_widths[col] = len(col)
        # Check data for this column
        for row in data:
            if col in row and row[col] is not None:
                col_widths[col] = max(col_widths[col], len(str(row[col])))
        # Add some padding
        col_widths[col] = min(col_widths[col] + 2, 30)
    
    # Print header
    header = " | ".join([f"{col:<{col_widths[col]}}" for col in columns])
    print(header)
    print("-" * len(header))
    
    # Print rows
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
    """Get confirmation from user"""
    response = input(f"{prompt} (yes/no): ").strip().lower()
    return response in ['yes', 'y']

def format_name(user):
    """Format user name from dictionary"""
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
    """Format club display"""
    name = club.get('name', 'Unknown')
    status = club.get('activity_status', '')
    club_id = club.get('club_id', '')
    
    if status:
        return f"{name} [{status}] (ID: {club_id})"
    return f"{name} (ID: {club_id})"