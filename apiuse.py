import databasing
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
from client import *
from clientsetup import userID, sp
from urllib.error import HTTPError

def getRecents(checklimit=10):
    results = sp.current_user_recently_played(limit=checklimit)
    recentTracks = []
    trackIDList = []
    for item in results['items']:
        currentTrack = {}
        track = item['track']
        trackID = track['id']
        currentTrack['name'] = track['name']
        currentTrack['artist'] = track['artists'][0]['name']
        currentTrack['id'] = trackID
        trackDetails = sp.track(trackID)
        currentTrack["image"] = trackDetails['album']['images'][0]['url']
        recentTracks.append(currentTrack)
        trackIDList.append(trackID)
    databasing.saveTracktoDB(trackIDList)
    return recentTracks


def getTop(checklimit=10, timeframe="medium_term"):
    results = sp.current_user_top_tracks(limit=checklimit, time_range=timeframe)
    topTracks = []
    trackIDList = []
    for track in results['items']:
        currentTrack = {}
        trackID = track['id']
        currentTrack['name'] = track['name']
        currentTrack['artist'] = track['artists'][0]['name']
        currentTrack['id'] = trackID
        trackDetails = sp.track(trackID)
        currentTrack["image"] = trackDetails['album']['images'][0]['url']
        topTracks.append(currentTrack)
        trackIDList.append(trackID)
    databasing.saveTracktoDB(trackIDList)
    return topTracks

def getLibrary(limit = 10):
    results = sp.current_user_saved_tracks(limit)
    libraryTracks = []
    trackIDList = []
    for item in results['items']:
        currentTrack = {}
        track = item['track']
        trackID = track['id']
        currentTrack['name'] = track['name']
        currentTrack['artist'] = track['artists'][0]['name']
        currentTrack['id'] = trackID
        trackDetails = sp.track(trackID)
        currentTrack["image"] = trackDetails['album']['images'][0]['url']
        libraryTracks.append(currentTrack)
        trackIDList.append(trackID)
    databasing.saveTracktoDB(trackIDList)
    return libraryTracks

def getRecommendations(baseTrack, recommnendNum):
    recommendedTracks = sp.recommendations(seed_tracks=baseTrack, limit=recommnendNum)
    recommendations = []
    for track in recommendedTracks['tracks']:
        currentTrack = {}
        trackID = track['id']
        currentTrack['name'] = track["name"]
        currentTrack['artist'] = track["artists"][0]["name"]
        currentTrack['id'] = trackID
        currentTrack['url'] = track['external_urls']['spotify']
        trackDetails = sp.track(trackID)
        currentTrack["image"] = trackDetails['album']['images'][0]['url']
        recommendations.append(currentTrack)
    return recommendations

def getPlaylists(getLimit=10):
    userPlaylists = sp.user_playlists(user=userID, limit=getLimit)
    playlists= []
    for playlist in userPlaylists['items']:
        currentPlaylist = {}
        currentPlaylist['name'] = playlist['name']
        currentPlaylist['id'] = playlist['id']
        try:
            currentPlaylist['image'] = playlist['images'][0]['url']
        except IndexError:
            pass
        playlists.append(currentPlaylist)
        getPlaylistItems(playlist['id'])
    return playlists


def getPlaylistItems(playlistID):
    trackIDs = []
    response = sp.playlist_items(playlistID)
    c = 0
    while c != int(response['total']):
        if c == 100:
            break
        trackIDs.append(response['items'][c]['track']['id'])
        c+= 1
    databasing.savePlaylistItemsToDB(playlistID,trackIDs)

def createPlaylist(name, description="", publicStatus=False):
    response = sp.user_playlist_create(userID, name, publicStatus, description=description)
    if response['id']:
        return response['id']
    else:
        return False

def addTrack(playlistID, trackIDs):
    trackURI = []
    trackJSON = sp.tracks(trackIDs)
    c = 0
    for track in trackJSON["tracks"]:
        trackURI.append(trackJSON["tracks"][c]["uri"])
        c += 1
    playlistLength = sp.playlist_items(playlist_id=playlistID,fields="total")['total']
    response = sp.playlist_add_items(playlist_id=playlistID,items=trackURI, position=playlistLength)
    if response["snapshot_id"]:
        return True
    else:
        return False

def generalSearch(query, limit=5):
    results = sp.search(query,limit, type='track')
    allResults = []
    for typeResult in results:
        resultType = results[typeResult]
        for itemResult in resultType["items"]:
           searchResult = {}
           trackID = itemResult['id']
           searchResult['id'] = trackID
           searchResult['name'] = itemResult['name']
           searchResult['artist'] = itemResult['artists'][0]['name']
           searchResult['album'] = itemResult['album']['name']
           trackDetails = sp.track(trackID)
           searchResult["image"] = trackDetails['album']['images'][0]['url']
           allResults.append(searchResult)
    return allResults

def getPlaylistName(playlistID):
    try:
        results = sp.playlist(playlistID)
        return {"playlistName":results['name'], 
                "url":results["external_urls"]["spotify"],
                "image":results["images"][0]["url"]
                }
    except HTTPError as err:
        return {"error":err}
