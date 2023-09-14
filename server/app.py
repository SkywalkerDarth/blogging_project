from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import LoginManager, login_user, login_required, UserMixin
from flask_bcrypt import Bcrypt
import json


app = Flask(__name__)
app.secret_key = '111'
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)


DATA_FILE = 'users.json'


class User(UserMixin):
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username


@login_manager.user_loader
def load_user(user_id):
    user_data = get_user_by_id(user_id)
    if user_data:
        return User(user_data['id'], user_data['username'])
    return None


def get_user_by_id(user_id):
    try:
        with open(DATA_FILE, 'r') as file:
            users_data = json.load(file)
            return users_data.get(str(user_id))
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


def write_user(user_id, user_data):
    users = read_users()
    users.append(user_data)
    with open(DATA_FILE, 'w') as file:
        json.dump({'users': users}, file)


def delete_user(user_id):
    users = read_users()
    if user_id in users:
        del users[user_id]
        with open(DATA_FILE, 'w') as file:
            json.dump(users, file)
        return True
    else:
        return False


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = get_user_by_id(user_id)

        if user and bcrypt.check_password_hash(user['password'], password):
            login_user(User(user['id'], user['username']))
            flash('Sign in successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'error')
            return render_template('login.html')

    return render_template('login.html')



@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        users = read_users()

        if any(user['username'] == username for user in users):
            return render_template('signup.html', error='Username already taken, please try another username')

        user_id = str(len(users) + 1)
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = {'id': user_id, 'username': username, 'password': hashed_password}

        write_user(user_id, user)
        flash('Signup successful! Please log in.', 'success')

        return redirect(url_for('login'))

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

