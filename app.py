from flask import Flask, request, url_for
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = "80hruivnghreuiwofl085"
app.config["SESSION_COOKIE_NAME"] = "Ciaran's Cookie"

@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirect():
    return "redirect"

@app.route('/get-tracks')
def getTracks():
    return "Some of Ciaran's Songs"

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=os.environ["CLIENT_ID"],
        client_secret=os.environ["CLIENT_SECRET"],
        redirect_uri=url_for('redirect', _external=True),
        scope="user-library-read"
    )