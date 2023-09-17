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
                return users.get('users', {})
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def write_users(self, users):
        with open(self.DATA_FILE, 'w') as file:
            json.dump({'users': users}, file)

    def get_user_by_id(self, user_id):
        users = self.read_users()
        return users.get(user_id)

    def get_user_by_username(self, username):
        users = self.read_users()
        return next((user for user in users.values() if user['username'] == username), None)


    def update_password(self, username, new_hashed_password):
        users = self.read_users()
        updated_users = {user_id: {'id': user['id'], 'username': user['username'], 'password': new_hashed_password}
                         for user_id, user in users.items() if user['username'] == username}
        self.write_users(updated_users)

    def delete_user(self, username):
        users = self.read_users()
        updated_users = {user_id: user for user_id, user in users.items() if user['username'] != username}
        self.write_users(updated_users)

    def generate_user_id(self):
        users = self.read_users()
        return str(len(users) + 1)

    def hash_password(self, password):
        return self.bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, hashed_password, input_password):
        return self.bcrypt.check_password_hash(hashed_password, input_password)
