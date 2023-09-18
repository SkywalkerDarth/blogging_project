from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from flask_login import LoginManager, login_user, login_required, UserMixin, logout_user, current_user
from user_manager import UserManager

app = Flask(__name__)
app.secret_key = '122333444455555666666777777788888888999999999'
login_manager = LoginManager()
login_manager.init_app(app)

user_manager = UserManager('users.json')

class User(UserMixin):
    def __init__(self, user_id, username, password):
        self.id = user_id
        self.username = username
        self.password = password


@login_manager.user_loader
def load_user(user_id):
    user_data = user_manager.get_user_by_id(user_id)
    if user_data:
        return User(user_id, user_data['username'], user_data['password'])
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
            user_id = user['id']
            login_user(User(user_id, username, user['password']))
            flash('Sign in successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'error')

    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if user_manager.get_user_by_username(username):
            flash('Username already taken, please try another username', 'error')
        else:
            user_id = str(user_manager.generate_user_id())
            hashed_password = user_manager.hash_password(password)
            user = {'id': user_id, 'username': username, 'password': hashed_password}

            users = user_manager.read_users()
            users[user_id] = user
            user_manager.write_users(users)

            flash('Signup successful! Please log in.', 'success')
            return redirect(url_for('login'))

    return render_template('signup.html')



@app.route('/api/get_username', methods=['GET'])
@login_required
def get_username():
        return jsonify({'username': current_user.username})


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))


@app.route('/change_password', methods=['POST', 'GET'])
@login_required
def change_password():
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')

        if user_manager.check_password(current_user.password, old_password):
            new_hashed_password = user_manager.hash_password(new_password)
            user_manager.update_password(current_user.username, new_hashed_password)
            flash('Password changed successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid old password. Please try again.', 'error')

    return render_template('change_password.html')


@login_required
@app.route('/engineering')
def engineering():
    return render_template('engineering.html')


@login_required
@app.route('/history')
def history():
    return render_template('history.html')


@login_required
@app.route('/stories')
def stories():
    return render_template('stories.html')


@login_required
@app.route('/sciences')
def sciences():
    return render_template('sciences.html')


@login_required
@app.route('/sports')
def sports():
    return render_template('sports.html')


if __name__ == '__main__':
    app.run(debug=True)
