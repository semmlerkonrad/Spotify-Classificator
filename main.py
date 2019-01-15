from flask import Flask, redirect
import getData
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
    return redirect(getData.redirectURI)

@app.route("/callback/q")
def callback():
    authToken = getData.getAuthToken()

    listAllData=[]
    getData.getTrackAndAlbumIDsFromPlaylist('37i9dQZF1DX2vTOtsQ5Isl', authToken, 'pop')
    playlistIDs = {
        #'37i9dQZF1DX2vTOtsQ5Isl':'Pop',
        #'37i9dQZF1DX0XUsuxWHRQd':'Rap',
        # '37i9dQZF1DWXRqgorJj26U':'Rock',
        #'37i9dQZF1DX3xuESxW8V9F':'EDM',
                   # '37i9dQZF1DXa8NOEUWPn9W':'House',
                   # '37i9dQZF1DX6J5NfMJS675':'Techno',
                   # '37i9dQZF1DXbXD9pMSZomS':'Lo-fi House',
                   # '37i9dQZF1DXbITWG1ZJKYt':'Jazz'
    }

    for playlist, genre in playlistIDs.items():
        currentTracks = getData.getTrackAndAlbumIDsFromPlaylist(playlist, authToken, genre)
        listAllData+=currentTracks

    cols = ['trackID', 'albumID', 'track Genre', 'duration', 'end Of Fade-In', 'start Of Fade-Out', 'loudness', 'tempo',
            'time Signature', 'mode', 'key', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness',
            'speechiness', 'valence', 'number Of Sections']
    dataAll = pd.DataFrame(listAllData, columns=cols)
    dataAll.to_csv('newcsv3.csv')
    return "done"


if __name__ == "__main__":
    # po włączeniu wchodzimy na "http://127.0.0.1:8080" żeby wykonać zapytania zapisane w callback()
    app.run(debug=True,port=8080)