import spotifyMining
import pandas as pd

# TODO add docstrings
# TODO Get several artists
# TODO sections of songs
# TODO maybe it'll be better to get genre through the playlist category

authToken = spotifyMining.getAuthToken()

listAllData = []
playlistIDs = {
    #'37i9dQZF1DX2vTOtsQ5Isl':'Pop',
    # '37i9dQZF1DX0XUsuxWHRQd':'Rap',
    # '37i9dQZF1DWXRqgorJj26U':'Rock',
    # '37i9dQZF1DX3xuESxW8V9F': 'EDM',
    # '37i9dQZF1DXa8NOEUWPn9W':'House',
    # '37i9dQZF1DX6J5NfMJS675':'Techno',
    # '37i9dQZF1DXbXD9pMSZomS':'Lo-fi House',
    # '37i9dQZF1DXbITWG1ZJKYt':'Jazz'
}

cols = ['trackID', 'albumID', 'track Genre', 'duration', 'end Of Fade-In', 'start Of Fade-Out', 'loudness', 'tempo',
        'time Signature', 'mode', 'key', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness',
        'speechiness', 'valence', 'number Of Sections']

for playlist, genre in playlistIDs.items():
    currentTracks = spotifyMining.getTrackAndAlbumIDsFromPlaylist(playlist, authToken, genre)
    listAllData += currentTracks

dataAll = pd.DataFrame(listAllData, columns=cols)
with open('newcsv6.csv', 'a') as outCSV:
    dataAll.to_csv(outCSV, index=False, header=False)
