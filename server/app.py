from flask import Flask, render_template, request, flash, redirect, session, url_for
import json
import os
from flask_login import LoginManager, login_user, login_required


app = Flask(__name__)
app.secret_key = ''
DATA_FILE = 'users.json'

login_manager = LoginManager()
login_manager.init_app(app)



class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    with open('DATA_FILE', 'r') as file:
        users_data = json.load(file)['users']
        for user_data in users_data:
            if user_data['id'] == user_id:
                return User(user_data['id'], user_data['username'], user_data['password'])
    return None


def read_users():
    try:
        with open(DATA_FILE, 'r') as file:
            users = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        users = []
    return users


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Retrieve the users from the data file
        users = read_users()

        # Check if the username and password match
        for user in users:
            if user['username'] == username and user['password'] == password:

                login_user(user, remember=True)  # This remembers the user if True
                return redirect(url_for('dashboard'))

                # Redirect to the user profile page if the login is successful

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
            # Create a new user object
            user = {'username': username, 'password': password}
            # Store the user object in the data file
            users.append(user)
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


if __name__ == '__main__':
    app.run(debug=True)
