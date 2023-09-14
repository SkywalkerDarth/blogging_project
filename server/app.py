from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import LoginManager, login_user, login_required, UserMixin
from user_manager import UserManager

app = Flask(__name__)
app.secret_key = '111'
login_manager = LoginManager()
login_manager.init_app(app)

user_manager = UserManager('users.json')

class User(UserMixin):
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    user_data = user_manager.get_user_by_id(user_id)
    if user_data:
        return User(user_data['id'], user_data['username'])
    return None




@app.route('/')
def index():
    return render_template('index.html')



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = user_manager.get_user_by_username(username)

        if user and user_manager.check_password(user['password'], password):
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

        users = user_manager.read_users()

        if any(user['username'] == username for user in users):
            return render_template('signup.html', error='Username already taken, please try another username')

        user_id = str(len(users) + 1)
        hashed_password = user_manager.hash_password(password)
        user = {'id': user_id, 'username': username, 'password': hashed_password}

        user_manager.write_user(user)
        flash('Signup successful! Please log in.', 'success')

        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/engineering')
def engineering():
    return render_template('engineering.html')


@app.route('/history')
def history():
    return render_template('history.html')


@app.route('/stories')
def stories():
    return render_template('stories.html')


@app.route('/sciences')
def sciences():
    return render_template('sciences.html')

@app.route('/sports')
def sports():
    return render_template('sports.html')

if __name__ == '__main__':
    app.run(debug=True)
