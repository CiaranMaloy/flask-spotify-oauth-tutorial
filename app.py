from flask import Flask, request, url_for, session, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import time

load_dotenv()

app = Flask(__name__)
app.secret_key = "80hruivnghreuiwofl085"
app.config["SESSION_COOKIE_NAME"] = "Ciaran's Cookie"
TOKEN_INFO = "token_info"

@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('getTracks'))

@app.route('/get-tracks')
def getTracks():
    try:
      token_info = get_token()
    except:
        print("user not logged in")
        redirect(url_for("login", _external=False))

    sp = spotipy.Spotify(auth=token_info['access_token'])
    tracks = sp.current_user_saved_tracks(limit=50, offset=0)
    for i in range(0, 50):
        print(tracks['items'][i]['track']['name'], tracks['items'][i]['track']['artists'][0]['name'])
    return sp.current_user_saved_tracks(limit=50, offset=0)

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise "exception"
    
    now = int(time.time())
    is_expired = token_info["expires_at"] - now < 60
    if is_expired:
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])
    return token_info

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=os.environ["CLIENT_ID"],
        client_secret=os.environ["CLIENT_SECRET"],
        redirect_uri=url_for('redirectPage', _external=True),
        scope="user-library-read"
    )