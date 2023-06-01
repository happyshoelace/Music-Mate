import pprint
from psycopg2 import *
import psycopg2
from clientsetup import userID
from client import *

def saveTracktoDB(trackID):
    try:
        # Connect to an existing database
        connection = psycopg2.connect(user=dbuser,
                                    password=dbpass,
                                    host=dbHost,
                                    port=dbPort,
                                    dbname = dbName)

        # Create a cursor to perform database operations
        cursor = connection.cursor()
        
        inDB = False

        cursor.execute("SELECT * FROM public.tracks;")
        tracks = cursor.fetchall()
        for results in tracks:
            if results[0] == trackID:
                inDB = True
                break
        if inDB == False:
            cursor.execute(f"INSERT INTO public.tracks (track_id) VALUES ('{trackID}')")
            connection.commit()

        cursor.execute(f"INSERT INTO public.user_tracks (track_id, user_id) VALUES ('{trackID}', '{userID}')")
        connection.commit()

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()


def savePlaylistItemsToDB(playlistID, trackIDs):
    try:
        # Connect to an existing database
        connection = psycopg2.connect(user=dbuser,
                                    password=dbpass,
                                    host=dbHost,
                                    port=dbPort,
                                    dbname = dbName)

        # Create a cursor to perform database operations
        cursor = connection.cursor()
        
        inDB = False

        cursor.execute("SELECT * FROM public.playlists;")
        playlists = cursor.fetchall()
        for results in playlists:
            if results[0] == playlistID:
                inDB = True
                break
        if inDB == False:
            cursor.execute(f"INSERT INTO public.playlists (playlist_id) VALUES ('{playlistID}')")
            connection.commit()
            cursor.execute("SELECT * FROM public.tracks;")
            recordedTracks = cursor.fetchall()
            for trackID in trackIDs:
                inDB = False
                for recordedTrackID in recordedTracks:
                    if recordedTrackID[0] == trackID:
                        inDB = True
                        break
                if inDB == False:
                    cursor.execute(f"INSERT INTO public.tracks (track_id) VALUES ('{trackID}')")
                    connection.commit()
                cursor.execute(f"INSERT INTO public.playlist_tracks (track_id, playlist_id) VALUES ('{trackID}' , '{playlistID}')")
                connection.commit()
                cursor.execute(f"INSERT INTO public.user_tracks (track_id, user_id) VALUES ('{trackID}' , '{userID}')")
                connection.commit()
        else:
            print("Already in DB")


    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()

def readTracksFromDB(trackID):
    try:
        # Connect to an existing database
        connection = psycopg2.connect(user=dbuser,
                                    password=dbpass,
                                    host=dbHost,
                                    port=dbPort,
                                    dbname = dbName)

        # Create a cursor to perform database operations
        cursor = connection.cursor()

        response = {}

        cursor.execute(f"SELECT * FROM public.user_tracks WHERE track_id = '{trackID}'")
        results = cursor.fetchall()
        trackListeners = {}
        try:
            for result in results:
                user = result[2]
                if user not in trackListeners:
                    trackListeners[user] = 1
                else:
                    templistens = trackListeners[user]
                    trackListeners[user] = templistens+1
            response['registered listeners'] = trackListeners

            cursor.execute(f"SELECT * FROM public.user_tracks WHERE track_id = '{trackID}' AND user_id = '{userID}'")
            results = cursor.fetchall()
            c = 0
            for result in results:
                time = str(result[3])
                if c == 0:
                    response['first recorded'] = time[:10]
                elif c == len(results)-1:
                    response['most recent record'] = time[:10]
                c+=1

            return response   
        except TypeError:
            return "Hmmm, looks like we don't have this recorded in our database! (Hint: Choose option 3 on the main screen to do a track/playlist update)"

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()

def readPlaylistsFromDB(trackID):
    try:
        # Connect to an existing database
        connection = psycopg2.connect(user=dbuser,
                                    password=dbpass,
                                    host=dbHost,
                                    port=dbPort,
                                    dbname = dbName)

        # Create a cursor to perform database operations
        cursor = connection.cursor()

        cursor.execute(f"SELECT playlist_id FROM playlist_tracks WHERE track_id = '{trackID}'")
        results = cursor.fetchall()
        returnableList = []
        for result in results:
            if result not in returnableList:
                returnableList.append(result)

        return returnableList
        

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()

