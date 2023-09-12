from flask import Flask, render_template, request, flash, redirect, session, url_for
import json
import os
from flask_login import LoginManager, login_user, login_required
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.secret_key = ''
bcrypt = Bcrypt(app)
DATA_FILE = 'users.json'

login_manager = LoginManager()
login_manager.init_app(app)


class User:
    def __init__(self, username):
        self.username = username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username


def get_user_data_by_username(username):
    try:
        with open('DATA_FILE', 'r') as file:
            users_data = json.load(file)['users']
            for user_data in users_data:
                if user_data['username'] == username:
                    return user_data
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error: Unable to decode JSON data")

    return None



def load_user(username):
    # Load the user based on the username
    user_data = get_user_data_by_username(username)
    if user_data:
        return User(user_data['username'])
    return None



def read_users():
    try:
        with open(DATA_FILE, 'r') as file:
            users = json.load(file)
            return users.get('users', [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []



def write_users(users):
    with open(DATA_FILE, 'w') as file:
        json.dump(users, file)



def delete_users(username):
    users = read_users()
    updated_users = [user for user in users if user['username'] != username]
    write_users(updated_users)


#Routes#


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Retrieve the users from the data file
        users = read_users()

        # Check if the username exists
        user = next((user for user in users if user['username'] == username), None)

        if user and check_password_hash(user['password'], password):
            # If the username and password are correct, log the user in
            login_user(User(user['username']))

            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid username or password')

    # If GET request, render the login page
    return render_template('login.html')



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')     
        users = read_users()

        if any(user['username'] == username for user in users):
            return render_template('signup.html', error='Username already taken, please try another username')

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create a new user object
        user = {'username': username, 'password': hashed_password}

        # Add the user to the list of users
        users.append(user)

        # Write the updated list of users to the file
        write_users(users)

        return render_template('login.html')

    return render_template('signup.html')



@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')



@app.route('/recovery')
def recovery():
    return render_template('recovery.html')



@app.route('/login/first_page')
def first_page():
    return render_template('first_page.html')


if __name__ == '__main__':
    app.run(debug=True)
