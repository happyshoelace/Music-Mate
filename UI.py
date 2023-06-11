from flask import Flask, flash, render_template, redirect,request
import clientsetup
import apiuse
import databasing
import spotipy
from urllib.error import HTTPError

app = Flask(__name__)

@app.route('/')
def signIn():
    return render_template('index.html')

@app.route('/authenticateUser/')
def authenticateUser():
    global sp; sp=clientsetup.initalise()
    return redirect('/home/')

@app.route('/home/')
def home():
    try:
        userInfo = sp.me()
        userName = userInfo['display_name']
        userImage = userInfo['images'][0]['url']
        return render_template('home.html',userName=userName, userImage=userImage)
    except NameError:
        return redirect('/authenticateUser/')

@app.route('/playlistBySearch/')
def playlistBySearch():
    return render_template('playlistBySearchIndex.html')
    
@app.route('/searchTracks/', methods=["GET","POST"])
def searchTracks():
    if request.method == 'POST':
        searchQuery = request.form.get('searchQuery')
        searchResults = apiuse.generalSearch(searchQuery, 15)
        print(searchResults)
        return render_template('playlistBySearchResults.html', searchResults=searchResults)
    else:
        return render_template('err.html')

@app.route('/findPlaylists/', methods=["GET","POST"])
def findPlaylists():
    trackID = request.form.get('trackValue')
    try:
        trackDetails = sp.track(trackID)
    except NameError:
        sp=clientsetup.initalise()
        trackDetails = sp.track(trackID)
    finally:
        trackDetails = sp.track(trackID)
        trackName = trackDetails["name"]
        trackArtist = trackDetails['artists'][0]['name']
        trackAlbum = trackDetails["album"]['name']
        trackURL = trackDetails["external_urls"]["spotify"]
        trackImage = trackDetails['album']['images'][0]['url']
        trackDBSearch = databasing.readTracksFromDB(trackID)
        playlistID = databasing.readPlaylistsFromDB(trackID)
        playlistList = []
        registeredListeners = 0
        userPlays = 0
        userInfo = sp.me()
        userName = userInfo['id']
        recordedTrack = False
        timeResponse = ""
        for user in trackDBSearch['registered listeners']:
            registeredListeners += 1
            if user == userName:
                userPlays = trackDBSearch['registered listeners'][user]
                recordedTrack = True
        if recordedTrack:
            firstRecord = trackDBSearch['first recorded']
            lastRecord = trackDBSearch['most recent record']
            timeResponse = f"The first time you logged it was on {firstRecord}, and the most recent time was {lastRecord}!"
        for playlist in playlistID:
            try:
                playlistInfo = apiuse.getPlaylistName(playlist[0])
                playlistList.append(playlistInfo)
            except (spotipy.SpotifyException, HTTPError) as err:
                print(err)
        return render_template('playlistBySearchFinalDisplay.html', userPlays=userPlays, timeResponse=timeResponse, trackID=trackID, trackName=trackName, trackAlbum=trackAlbum, trackArtist=trackArtist,trackImage=trackImage, trackURL= trackURL, trackDBSearch=trackDBSearch, playlistList=playlistList)

@app.route('/playlistByRecommendation/')
def playlistByRecommendation():
    topTracks = apiuse.getTop(25, "short_term")
    recentTracks = apiuse.getRecents(25)
    library = apiuse.getLibrary(25)
    return render_template('playlistByRecommendationIndex.html', topTracks=topTracks, recentTracks=recentTracks, library=library)

@app.route('/generateRecommendations/', methods=['GET', 'POST'])
def generateRecommendations():
    if request.method == 'POST':
        global trackID; trackID = [request.form.get('trackValue')]
        recommendations = apiuse.getRecommendations(trackID,25)
        return render_template('generateRecommendations.html', recommendations=recommendations)
    else:
        try:
            trackID = [request.form.get('trackValue')]
            recommendations = apiuse.getRecommendations(recommendationIDs,5)
            return render_template('generateRecommendations.html', recommendations=recommendations)
        except NameError:
            return render_template('err.html')
    
@app.route('/getPlaylists/', methods=['GET','POST'])
def getPlaylists():
    if request.method == 'POST':
        global recommendationIDs; recommendationIDs = request.form.getlist('recommendedTrack')
        playlists = apiuse.getPlaylists(25)
        return render_template('recommendationsGetPlaylist.html', playlists=playlists)
    else:
        return render_template('err.html')
    
@app.route('/createPlaylist/', methods=['POST','GET'])
def createPlaylist():
    if request.method == 'POST':
        playlistName = request.form.get('playlistName')
        playlistDescription = request.form.get('playlistDescription')
        playlistStatus = request.form.get('playlistStatus')
        if playlistStatus == 'True':
            playlistStatus = True
        else:
            playlistStatus = False
        global playlistID
        playlistID = apiuse.createPlaylist(playlistName, playlistDescription, playlistStatus)
        if playlistID:
            return redirect('/addToPlaylist/')
        else:
            flash("Hmm, something went wrong.")
            return redirect('/home/')
    else:
        return render_template('err.html')

@app.route('/addToPlaylist/', methods=['POST','GET'])
def addToPlaylists():
    global recommendationIDs
    global trackID
    global playlistID

    if request.method == 'POST':
        playlistID = request.form.get('playlistValue')

        recommendationIDs.append(trackID[0])
        response = apiuse.addTrack(playlistID,recommendationIDs)
        if response:
            return render_template('playlistAddSuccess.html')
        else:
            flash("Hmm, something went wrong.")
            return redirect('/home/')
    else:
        try:
            recommendationIDs.append(trackID[0])
            response = apiuse.addTrack(playlistID,recommendationIDs)
            del recommendationIDs
            del trackID
            del playlistID
            if response:
                return render_template('playlistAddSuccess')
            else:
                flash("Hmm, something went wrong.")
                return redirect('/home/')
        except NameError:
            return render_template('err.html')
            
@app.errorhandler(404)
def error404(e):
    return render_template('err.html')

if __name__ == '__main__':
    app.run(debug=True)
