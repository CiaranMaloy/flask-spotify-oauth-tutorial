from flask import Flask, request, url_for
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)
app.secret_key = "80085"
app.config["SESSION_COOKIE_NAME"] = "Ciaran's Cookie"

@app.route('/')
def index():
    return "Ciaran's Home Page"

@app.route('/get-tracks')
def getTracks():
    return "Some of Ciaran's Songs"