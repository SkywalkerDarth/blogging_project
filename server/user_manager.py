import json
from flask_bcrypt import Bcrypt


class UserManager:
    def __init__(self, data_file):
        self.DATA_FILE = data_file
        self.bcrypt = Bcrypt()

    def read_users(self):
        try:
            with open(self.DATA_FILE, 'r') as file:
                users = json.load(file)
                return users.get('users', [])
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def write_user(self, user_data):
        users = self.read_users()
        users.append(user_data)
        with open(self.DATA_FILE, 'w') as file:
            json.dump({'users': users}, file)

    def get_user_by_id(self, user_id):
        try:
            with open(self.DATA_FILE, 'r') as file:
                users_data = json.load(file)
                return users_data.get(str(user_id))
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error: Unable to decode JSON data")
        return None

    def get_user_by_username(self, username):
        try:
            with open(self.DATA_FILE, 'r') as file:
                users_data = json.load(file)
                for user in users_data.get('users', []):
                    if user['username'] == username:
                        return user
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error: Unable to decode JSON data")
        return None

    def delete_user(self, username):
        users = self.read_users()
        updated_users = [user for user in users if user['username'] != username]
        with open(self.DATA_FILE, 'w') as file:
            json.dump({'users': updated_users}, file)

    def hash_password(self, password):
        return self.bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, hashed_password, input_password):
        return self.bcrypt.check_password_hash(hashed_password, input_password)
