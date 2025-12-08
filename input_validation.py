# utils/input_validation.py
def get_integer_input(prompt, min_val=None, max_val=None, default=None):
    while True:
        try:
            value = input(prompt).strip()
            
            # Handle empty input with default
            if not value and default is not None:
                return default
            
            value = int(value)
            
            if min_val is not None and value < min_val:
                print(f"Value must be at least {min_val}")
                continue
                
            if max_val is not None and value > max_val:
                print(f"Value must be at most {max_val}")
                continue
                
            return value
            
        except ValueError:
            print("Please enter a valid number.")

def get_date_input(prompt, allow_empty=False):
    import re
    date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    
    while True:
        value = input(prompt).strip()
        
        if not value and allow_empty:
            return None
            
        if not date_pattern.match(value):
            print("Please enter date in YYYY-MM-DD format")
            continue
            
        # Basic validation (could add more thorough date validation)
        try:
            year, month, day = map(int, value.split('-'))
            if month < 1 or month > 12 or day < 1 or day > 31:
                print("Invalid date")
                continue
        except:
            print("Invalid date")
            continue
            
        return value

def get_datetime_input(prompt, allow_empty=False):
    import re
    datetime_pattern = re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$')
    
    while True:
        value = input(prompt).strip()
        
        if not value and allow_empty:
            return None
            
        if not datetime_pattern.match(value):
            print("Please enter datetime in YYYY-MM-DD HH:MM format")
            continue
            
        return value
    
def confirm_action(prompt="Are you sure?"):
    """Get confirmation from user"""
    response = input(f"{prompt} (yes/no): ").strip().lower()
    return response in ['yes', 'y']