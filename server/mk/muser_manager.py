import json
import hashlib

DATA_FILE = 'users.json'

def get_user_by_username(username):
    try:
        with open(DATA_FILE, 'r') as file:
            users_data = json.load(file)
            for user in users_data.get('users', []):
                if user['username'] == username:
                    return user
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error: Unable to decode JSON data")
    return None

def read_users():
    try:
        with open(DATA_FILE, 'r') as file:
            users = json.load(file)
            return users.get('users', [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def write_user(user_data):
    users = read_users()
    users.append(user_data)
    with open(DATA_FILE, 'w') as file:
        json.dump({'users': users}, file)

def delete_user(username):
    users = read_users()
    updated_users = [user for user in users if user['username'] != username]
    with open(DATA_FILE, 'w') as file:
        json.dump({'users': updated_users}, file)

def hash_password(password):
    salt = b'some_random_salt'
    hashed_password = hashlib.sha256(salt + password.encode('utf-8')).hexdigest()
    return hashed_password
