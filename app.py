#IMPORT DEPENDENCIES
from flask import Flask, url_for, render_template, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
import json
import sqlite3
import os
from oauthlib.oauth2 import WebApplicationClient
import requests
from db import init_db_command
from user import User

#CONFIG GOOGLE STUFF
GOOGLE_CLIENT_ID = "947866333045-2tjfigdp1cvp2148gv2il1p7oaep31t6.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = ''

db = SQLAlchemy(app)

class Clubs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    complete = db.Column(db.Boolean)

# User session management setup
login_manager = LoginManager()
login_manager.init_app(app)

# Naive database setup
try:
    init_db_command()
except sqlite3.OperationalError:
    # Assume it's already been created
    pass

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template("index.html")
    else:
        return render_template("signin.html")
    
def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@app.route('/routes')
def routes():
    if current_user.is_authenticated:
        return render_template("routes.html")
    else:
        return render_template("signin.html")
@app.route('/signin')
def signin():
    return render_template("signin.html")

@app.route('/profile')
def profile():
    if current_user.is_authenticated:
        return render_template("profile.html")
    else:
        return render_template("signin.html")

@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
    token_endpoint,
    authorization_response=request.url,
    redirect_url=request.base_url,
    code=code
    )
    token_response = requests.post(
    token_url,
    headers=headers,
    data=body,
    auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in your db with the information provided
    # by Google
    user = User(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    )

    # Doesn't exist? Add it to the database.
    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email, picture)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("index"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("signin"))

@app.route('/addClub', methods=['POST', 'GET'])
def addClub():
    if request.method == 'POST':
        clubName = request.form['club']


if __name__ == "__main__":
    app.run(debug=True)