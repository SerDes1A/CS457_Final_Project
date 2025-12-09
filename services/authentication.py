import bcrypt
from models.users import create_user, get_user_by_email

def hash_password(plain_password: str) -> str:
    return bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode()

def check_password(plain_password: str, hash: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hash.encode())

def register_user():
    while(1):
        email = input("Email: ").strip().lower()
        if get_user_by_email(email):
            print("User already exists.")
            return None
        elif email == "":
            print("An email address is needed.")
        elif '@' not in email:
            print("Please input a valid email address.")
        else:
            break
    
    while(1):
        password = input("Password: ").strip()
        if password == "":
            print("A password is needed")
        else:
            hashed_pwd = hash_password(password)
            break

    while(1):
        first = input("First Name: ").strip()
        last = input("Last Name: ").strip()
        if(first=="" or last==""):
            print("First/last name was left blank.")
        elif(not first.isalpha() or not last.isalpha()):
            print("Make sure there are no special characters in the first/last name.")
        else:
            break
    role = "student"

    new_user = create_user(email, hashed_pwd, first, last, role)
    print("Created user: ", new_user["user_id"], new_user["school_email"])
    return new_user

def login_user():
    max_attempts = 3
    
    for attempt in range(max_attempts):
        print(f"\nLogin Attempt {attempt + 1} of {max_attempts}")
        email = input("Email: ").strip().lower()
        user = get_user_by_email(email)
        
        if not user:
            print("No such user.")
            continue  # Try again
            
        password = input("Password: ").strip()
        if not check_password(password, user["password"]):
            print("Incorrect password.")
            if attempt < max_attempts - 1:
                print("Please try again.\n")
                import time
                time.sleep(1)  
            continue 
        
        print(f"\n✅ Welcome, {user.get('first_name') or user['school_email']}")
        return user

    print("\n❌ Too many failed attempts. Returning to main menu.")
    import time
    time.sleep(2) 
    return None