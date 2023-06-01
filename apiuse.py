import databasing
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
from client import *
import pprint
from clientsetup import userID, sp
from urllib.error import HTTPError


def getRecents(checklimit=10):
    results = sp.current_user_recently_played(limit=checklimit)
    recentTracks = []
    c = 1
    for item in results['items']:
        track = item['track']
        trackID = track['id']
        recentTracks.append(trackID)
        try:
            print(str(c)+". "+track["name"], "by", track["artists"]["name"])
        except TypeError:
            artistList = []
            for artists in track["artists"]:
                artistList.append(artists["name"])
            print(str(c)+". "+track["name"], "by", ', '.join(artistList))
        databasing.saveTracktoDB(trackID)
        c += 1
    return recentTracks

def getTop(checklimit=10, timeframe="medium_term"):
    results = sp.current_user_top_tracks(limit=checklimit, time_range=timeframe)
    topTracks = []
    c = 1
    for item in results['items']:
        try:
            print(str(c)+". "+item["name"], "by", item["artists"]["name"])
        except TypeError:
            artistList = []
            for artists in item["artists"]:
                artistList.append(artists["name"])
            print(str(c)+". "+item["name"], "by", ', '.join(artistList))
        trackID = item['id']
        topTracks.append(trackID)
        print(trackID)
        databasing.saveTracktoDB(trackID)
        c += 1
    return topTracks

def getLibrary(limit = 10):
    results = sp.current_user_saved_tracks(limit)
    libraryTracks = []
    c = 1
    for item in results['items']:
        try:
            print(str(c)+". "+item["track"]["name"], "by", item["track"]["artists"]["name"])
        except TypeError:
            artistList = []
            for artists in item["track"]["artists"]:
                artistList.append(artists["name"])
            print(str(c)+". "+item["track"]["name"], "by", ', '.join(artistList))
        trackID = item["track"]['id']
        libraryTracks.append(trackID)
        databasing.saveTracktoDB(trackID)
        c += 1
    return libraryTracks

def getRecommendations(baseTrack, recommnendNum):
    recommendedTracks = sp.recommendations(seed_tracks=baseTrack, limit=recommnendNum)
    recommendID = []
    print("Recommending...")
    c = 0
    for i in recommendedTracks['tracks']:
        recommendID.append(recommendedTracks['tracks'][c]['id'])
        try:
            print(str(c+1)+". "+recommendedTracks['tracks'][c]["name"], "by", recommendedTracks["tracks"][c]["artists"]["name"])
        except TypeError:
            artistList = []
            for artists in recommendedTracks["tracks"][c]["artists"]:
                artistList.append(artists["name"])
            print(str(c+1)+". "+recommendedTracks['tracks'][c]["name"], "by", ', '.join(artistList))
        c += 1
    return recommendID

def getPlaylists(getLimit=10):
    userPlaylists = sp.user_playlists(user=userID, limit=getLimit)
    playlistIDs = []
    print(userPlaylists['total'])
    c = 0
    for i in userPlaylists['items']:
        printedC = c + 1
        print(str(printedC)+". "+userPlaylists['items'][c]['name'])
        playlistIDs.append(userPlaylists["items"][c]["id"])        
        getPlaylistItems(userPlaylists["items"][c]["id"])
        c += 1
    return playlistIDs

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
    print(f"Created playlist called {name}")
    return response['id']

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
    searchIDs = []
    searchName = []
    c = 1
    for typeResult in results:
        resultType = results[typeResult]
        for itemResult in resultType["items"]:
           print(str(c)+".", itemResult["name"], "by", itemResult["artists"][0]["name"], "in", itemResult["album"]["name"], ":", itemResult["external_urls"]["spotify"])
           searchIDs.append(itemResult['id'])
           searchName.append(itemResult["name"])
           c +=1
    return searchIDs

def getPlaylistName(playlistID):
    try:
        results = sp.playlist(playlistID)
        return results['name'] + " : " + results["external_urls"]["spotify"]
    except HTTPError as err:
        print(err)
