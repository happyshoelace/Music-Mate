from __future__ import print_function
import pprint
from apiuse import *
from clientsetup import userName
from databasing import *


def recToPlaylistSequence ():
    print("First, pick where you want recommendations to come from: \n 1 - Recent Tracks \n 2 - Top Tracks \n 3 - Library")
    trackListSelect = int(input())
    if trackListSelect == 1:
        validInput = False
        while validInput != True:
            try:
                print("Good choice! How many do you want to see? (Pick a number between 1 and 50)")
                limit = int(input())
            except ValueError:
                print("I don't think that's a number... Try again!\n How many do you want to see?")
            else:
                validInput = True
        print("Awesome! Here are your recent tracks:")
        trackList = getRecents(limit)
    elif trackListSelect == 2:
        validInput = False
        while validInput != True:
            try:
                print("Good choice! How many do you want to see? (Pick a number between 1 and 50)")
                limit = int(input())
            except ValueError:
                print("I don't think that's a number... Try again!\n How many do you want to see?")
            else:
                validInput = True
        print("Okay! From which time period do you want to see? (OPTIONS: Short, Medium, Long)")
        timePeriod = input()
        validInput = False
        while validInput == False:
            match timePeriod.lower():
                case "short":
                    validInput = True
                    trackList = getTop(limit,"short_term")
                case "medium":
                    validInput = True
                    trackList = getTop(limit)
                case "long":
                    validInput = True
                    trackList = getTop(limit,"long_term")
                case other:
                    print("Hang on... I don't think that was one of the options, try again...")
                    timePeriod = input()
    elif trackListSelect == 3:
        validInput = False
        while validInput != True:
            try:
                print("Good choice! How many do you want to see? (Pick a number between 1 and 50)")
                limit = int(input())
            except ValueError:
                print("I don't think that's a number... Try again!\n How many do you want to see?")
            else:
                validInput = True
        print(f"Awesome! Here are {limit} recent additions to your library:")
        trackList = getRecents(limit)
    print("Groovy! Now pick a song to base recommendations on! (Use the number that correlates to the song)")
    selectedTrack = int(input())
    selectedTrackID = [trackList[selectedTrack-1]]
    print("I love that song! How many recommendations do you want? (Pick a number between 1 and 100)")
    limit = int(input())
    if limit < 1:
        limit = 1
    elif limit > 100:
        limit = 100
    recommendationIDs = getRecommendations(selectedTrackID, limit)
    print("Do you want to add these into a playlist? (Yes or no)")
    playlistAdditionConfirm = input().lower()
    if playlistAdditionConfirm == 'yes':
        print("Super! Do you want to add to a prexisting playlist or a make a new one? \n 1- Add to a Prexisting Playlist \n 2- Make a new playlist")
        playlistLocation = int(input())
        if playlistLocation == 1:
            print("Coolio! Here are your 10 most recent playlists...")
            playlistFetch = getPlaylists()
            print("Which playlist do you want to add these songs to? (Use the numbers that correlate to the name)")
            playlistToAdd = int(input())
            playlistIndex = playlistToAdd-1
            print(type(playlistIndex))
            addingPlaylistID = playlistFetch[playlistIndex]
            playlistAddSuccess = addTrack(addingPlaylistID, recommendationIDs)
            if playlistAddSuccess:
                print("Yay! Added the tracks!")
            else:
                print("Oh no! Something went wrong...")
        elif playlistLocation == 2:
            print("Sounds good! Let's make a new playlist together! What do you want to name it?")
            playlistName = input()
            while playlistName == "":
                print("Woah there champ, let's give this playlist a name!")
                playlistName = input()
            print("What about the description? (Note: Can be left blank)")
            playlistDescript = input()
            print("Do you want this playlist to be public? yes/no")
            playlistStatus = input().lower()
            while playlistStatus != "yes" and playlistStatus != "no":
                print("Buddy, this is important. Do you want this playlist to be public? yes/no")
                playlistStatus = input().lower()
            if playlistDescript:
                if playlistStatus == "yes":
                    newPlaylistID = createPlaylist(playlistName, playlistDescript, True)
                else:
                    newPlaylistID = createPlaylist(playlistName, playlistDescript)
            else:
                if playlistStatus == "yes":
                    newPlaylistID = createPlaylist(playlistName, publicStatus=True)
                else:
                    newPlaylistID = createPlaylist(playlistName)
            playlistAddSuccess = addTrack(newPlaylistID, recommendationIDs)
            if playlistAddSuccess:
                print("Yay! Added the tracks!")
            else:
                print("Oh no! Something went wrong...")

def searchSequence():
    print("Nice one! What is the name of what you're looking for?")
    query = input()
    while query == "":
        print("Kid. I need a name. I can find it with a name.")
        query = input()
    validInput = False
    while validInput == False:
        try:
            print("Perfect! Now how many do you want to see of each result? (Choose a number between 1 - 50)")
            searchLimit = int(input())
        except ValueError:
            print("I don't think that's a number... Try again!\n How many do you want to see of each result? (Choose a number between 1 - 50)")
        else:
            validInput = True
    print("That's it! Here are your results!")
    searchResults = generalSearch(query, searchLimit)
    print("Which one were you looking for (Please use the corresponding numbers)")
    searchedTrackNum = int(input())
    print("Cool! Here's some information about that track!")
    trackID = searchResults[searchedTrackNum-1]
    print(databasing.readTracksFromDB(trackID))
    recordedPlaylists = databasing.readPlaylistsFromDB(trackID)
    for playlistID in recordedPlaylists:
        try:
            playlistName = getPlaylistName(playlistID[0])
            print(playlistName)
        except spotipy.SpotifyException:
            pass


while True:
    print(f"Hi {userName}, let's get this party started!")
    print("What would you like to do? \n 1- Playlist Creator \n 2- Search Spotify \n 3- Exit")
    activitySelect = int(input())

    if activitySelect == 1:
        recToPlaylistSequence()
    elif activitySelect == 2:
        searchSequence()