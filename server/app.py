from flask import Flask, render_template, request, flash, redirect, session
import json
import os

app = Flask(__name__)
app.secret_key = '#######################'
DATA_FILE = 'users.json'


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


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

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
