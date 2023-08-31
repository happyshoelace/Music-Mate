# Music-Mate
Use the [Spotify API](https://developer.spotify.com/) and dedicated database to make and find Spotify playlist.

*Created for Information Process Technology final project.*

---
# How to Install

## Database
I don't include the database used in this project, to use this program, you need to make your own. I am using a PostgresSQL DB.

I use the following tables and columns:

**tracks**

|_ trackID Pk


**user_tracks**

|_ entryIndex Pk

|_ userID 

|_ trackID Fk

|_ entrydate


**playlists**

|_playlistID Pk
 
 
**playlist_tracks**

|_ trackID Fk

|_ playlistID Fk

## Dependencies
Furthermore, this program has the following dependencies:
1. Spotipy
2. psycopg2
3. Flask

Ensure you install these into your virtual environment using the requirements.txt file before running the program.
