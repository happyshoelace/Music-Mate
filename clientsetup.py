import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
from client import *

scope = "user-library-read user-library-modify "
scope += "user-read-currently-playing user-read-recently-played user-top-read "
scope += "playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public"
redirect_uri = "http://localhost:8080"


def initalise():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = ID, client_secret = Secret,redirect_uri = redirect_uri, scope=scope))
    return sp

sp = initalise()
userInfo = sp.me()
userName = userInfo['display_name']
userID = userInfo['id']