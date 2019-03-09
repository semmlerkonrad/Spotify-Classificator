from trackdigger import TrackDigger
import pandas as pd
from pathlib import Path
import os

# list of all songs from one genre; emptied when moving to the next one
list_all_data = []

# Specify how many songs you'd like to download at once (minimum is 100)
number_of_songs = 2000

# Specifies the CSV file to save data to (currently it saves to scripts directory)
csv_file = Path(os.path.dirname(os.path.realpath(__file__))).joinpath('SpotifyData.csv')

# Parameters Required for Authorization with Spotify API
CLIENT_ID = 'your client id'
CLIENT_SECRET = 'your client secret'

# column names for exporting to CSV
cols = ['Genre', 'duration', 'end Of Fade-In', 'start Of Fade-Out', 'loudness', 'tempo',
        'time Signature', 'mode', 'key', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness',
        'speechiness', 'valence', 'number Of Sections', 'tatums Per Beats', 'tatums Deviation', 'attack Average',
        'attack Deviation']

td = TrackDigger(CLIENT_ID, CLIENT_SECRET)
td.get_auth_token()
genres = td.get_genres()
number_of_songs /= 100

# You can specify from which genres you'd like to download recommended songs
for genre in genres[0:14]:
    for x in range(number_of_songs):
        print('Looking up Genre {0}; checkup {1}/{2}'.format(genre, x + 1, number_of_songs))
        current_tracks = td.get_tracks_and_their_data(genre)
        list_all_data += current_tracks

    # Creates a new DataFrame and dumps it to a CSV after completing one genre
    data_all = pd.DataFrame(list_all_data, columns=cols)
    if csv_file.is_file():
        with open(csv_file, mode='a') as outCSV:
            data_all.to_csv(outCSV, index=False, header=False)
    else:
        with open(csv_file, mode='w') as outCSV:
            data_all.to_csv(outCSV, index=False, header=True)

    print('Finished Genre {}'.format(genre))
    list_all_data = []
