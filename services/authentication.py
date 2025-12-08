import bcrypt
from models.users import create_user, get_user_by_email

def hash_password(plain_password: str) -> str:
    return bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode()

def check_password(plain_password: str, hash: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hash.encode())

def register_user():
    email = input("Email: ").strip().lower()
    if get_user_by_email(email):
        print("User already exists.")
        return None
    
    password = input("Passoword: ").strip()
    hashed_pwd = hash_password(password)

    first = input("First Name: ").strip()
    last = input("Last Name: ").strip()
    role = "student"

    new_user = create_user(email, hashed_pwd, first, last, role)
    print("Created user: ", new_user["user_id"], new_user["school_email"])
    return new_user

def login_user():
    email = input("Email: ").strip().lower()
    user = get_user_by_email(email)
    if not user:
        print("No such user.")
        return None
    
    password = input("Password: ").strip()
    if not check_password(password, user["password"]):
         print("Incorrect password.")
         return None
    
    print(f"Welcome, {user.get('first_name') or user['school_email']}")
    return user