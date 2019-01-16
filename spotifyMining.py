import requests
import base64
import time

#Wywaliłem hardcoded klucze, bo technicznie nie powinny być widoczne publicznie xd. Najłatwiej to samemu zamienić u siebie w edytorze
CLIENT_ID = input()
CLIENT_SECRET = input()

#Spotify and local URLS
SpotifyAuthorize = "https://accounts.spotify.com/authorize"
SpotifyToken = "https://accounts.spotify.com/api/token"
spotifyApi = "https://api.spotify.com/v1"

#Pobieramy Authorization Token z serwera Spotify
def getAuthToken():
    bodyPOST = {"grant_type": "client_credentials"}
    clientIdEncoded = "{}:{}".format(CLIENT_ID, CLIENT_SECRET).encode("ascii")
    base64encoded = base64.b64encode(clientIdEncoded)
    headers = {"Authorization": "Basic {}".format(base64encoded.decode('ascii'))}
    POSTrequest = requests.post(SpotifyToken, data=bodyPOST, headers=headers)
    checkForError(POSTrequest)

    # pobieramy Token z odpowiedzi serwera
    serverResponse = POSTrequest.json()
    accessToken = serverResponse["access_token"]

    # zapisujemy token do wszystkich przyszłych zapytań
    authHeader = {"Authorization":"Bearer {}".format(accessToken)}
    print('Connected to the Spotify Server')
    return authHeader

def getAudioAnalysis(trackID, authToken):
    #adres GET do wykonania tego zapytania, wystarczy podmienić ten adres na jakikolwiek inny podany w Docs i powinno działać
    chosenTrackEndpoint = "{0}/audio-analysis/{1}".format(spotifyApi, trackID)
    getRequest  = requests.get(chosenTrackEndpoint, headers = authToken)
    checkForError(getRequest)

    # dane z low-level analizy Audio zwrócone przez serwer
    analysisData = getRequest.json()
    return analysisData

def getAudioFeatures(trackID, authToken):
    chosenTrackEndpoint = "{0}/audio-features/{1}".format(spotifyApi, trackID)
    getRequest  = requests.get(chosenTrackEndpoint, headers = authToken)
    checkForError(getRequest)
    analysisData = getRequest.json()
    return analysisData

def getTrackAndAlbumIDsFromPlaylist(playlistID, authToken, genre):
    listOfID=[]

    chosenPlaylistEndpoint = "{0}/playlists/{1}/tracks".format(spotifyApi, playlistID)
    getRequest = requests.get(chosenPlaylistEndpoint, headers=authToken)
    checkForError(getRequest)

    print('Checking up playlist {}'.format(playlistID))
    playlistItems = getRequest.json()

    for item in playlistItems['items']:
        trackID = item['track']['id']
        albumID = item['track']['album']['id']
        try:
            trackAudioFeatures = getAudioFeatures(trackID, authToken)
            trackAudioData = getAudioAnalysis(trackID, authToken)

            duration = trackAudioData['track']['duration']
            endOfFadeIn = trackAudioData['track']['end_of_fade_in']
            startOfFadeOut = trackAudioData['track']['start_of_fade_out']
            loudness = trackAudioData['track']['loudness']
            tempo = trackAudioData['track']['tempo']
            timeSignature = trackAudioData['track']['time_signature']
            mode = trackAudioData['track']['mode']
            key = trackAudioFeatures['key']
            acousticness = trackAudioFeatures['acousticness']
            danceability = trackAudioFeatures['danceability']
            energy = trackAudioFeatures['energy']
            instrumentalness = trackAudioFeatures['instrumentalness']
            liveness = trackAudioFeatures['liveness']
            speechiness = trackAudioFeatures['speechiness']
            valence = trackAudioFeatures['valence']
            numberOfSections = len(trackAudioData['sections'])

            listOfID.append([trackID, albumID, genre, duration, endOfFadeIn, startOfFadeOut, loudness, tempo,
                             timeSignature, mode, key, acousticness, danceability, energy, instrumentalness, liveness,
                             speechiness, valence, numberOfSections])
        except notFoundException:
            print('Skipping track {}, as it does not have analysis data.'.format(trackID))

    print('Finished playlist {}'.format(playlistID))
    return listOfID

def getAlbumGenres(albumID, authToken):
    chosenAlbumEndpoint = "{0}/albums/{1}".format(spotifyApi, albumID)
    getRequest = requests.get(chosenAlbumEndpoint, headers=authToken)
    checkForError(getRequest)

    albumItems = getRequest.json()
    # with open('album.json', 'w') as outfile:
    #     json.dump(albumItems, outfile)
    firstGenre = albumItems['genres']
    if len(firstGenre)>0:
        firstGenre = firstGenre[0]
    else:
        firstGenre = 'None'
    return firstGenre

def checkForError(request):
    if not request.ok:
        if request.status_code == 429 :
            seconds = request.headers['Retry-After']
            print('Too Many Requests: waiting {} seconds.'.format(seconds))
            time.sleep(seconds)
        elif request.status_code == 404:
            if request.json()['error']['message'] == 'analysis not found':
                raise notFoundException

class notFoundException(Exception):
    """Raised when the current track does not have an analysis or features on the Spotify server"""