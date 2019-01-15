import json
import requests
import base64

#Wywaliłem hardcoded klucze, bo technicznie nie powinny być widoczne publicznie xd. Najłatwiej to samemu zamienić u siebie w edytorze
CLIENT_ID = input()
CLIENT_SECRET = input()

#Spotify URLS
authorizeURL = "https://accounts.spotify.com/authorize"
tokenURL = "https://accounts.spotify.com/api/token"
apiURL = "https://api.spotify.com/v1"

#Parametry servera
localURL = "http://127.0.0.1:8080"
redirectURI = "{}/callback/q".format(localURL)

#Pobieramy Authorization Token z serwera Spotify
def getAuthToken():
    bodyPOST = {"grant_type": "client_credentials"}
    clientIdEncoded = "{}:{}".format(CLIENT_ID, CLIENT_SECRET).encode("ascii")
    base64encoded = base64.b64encode(clientIdEncoded)
    headers = {"Authorization": "Basic {}".format(base64encoded.decode('ascii'))}
    POSTrequest = requests.post(tokenURL, data=bodyPOST, headers=headers)

    # pobieramy Token z odpowiedzi serwera
    serverResponse = json.loads(POSTrequest.text)
    accessToken = serverResponse["access_token"]

    # zapisujemy token do wszystkich przyszłych zapytań
    authHeader = {"Authorization":"Bearer {}".format(accessToken)}
    return authHeader

def getAudioAnalysis(trackID, authToken):
    #adres GET do wykonania tego zapytania, wystarczy podmienić ten adres na jakikolwiek inny podany w Docs i powinno działać
    chosenTrackEndpoint = "{0}/audio-analysis/{1}".format(apiURL, trackID)
    getRequest  = requests.get(chosenTrackEndpoint, headers = authToken)

    # dane z low-level analizy Audio zwrócone przez serwer
    analysisData = json.loads(getRequest.text)
    return analysisData

def getAudioFeatures(trackID, authToken):
    chosenTrackEndpoint = "{0}/audio-features/{1}".format(apiURL, trackID)
    getRequest  = requests.get(chosenTrackEndpoint, headers = authToken)
    analysisData = json.loads(getRequest.text)
    return analysisData

def getTrackAndAlbumIDsFromPlaylist(playlistID, authToken, genre):
    listOfID=[]

    chosenPlaylistEndpoint = "{0}/playlists/{1}/tracks".format(apiURL, playlistID)
    getRequest = requests.get(chosenPlaylistEndpoint, headers=authToken)

    playlistItems = json.loads(getRequest.text)
    # with open('error.json', 'w') as outfile:
    #     json.dump(playlistItems, outfile)
    if getRequest.ok:
        for item in playlistItems['items']:
            trackID = item['track']['id']
            albumID = item['track']['album']['id']

            trackAudioFeatures = getAudioFeatures(trackID,authToken)
            trackAudioData = getAudioAnalysis(trackID,authToken)

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

            listOfID.append([trackID,albumID, genre, duration, endOfFadeIn, startOfFadeOut, loudness, tempo,
                             timeSignature, mode, key, acousticness, danceability, energy, instrumentalness, liveness,
                             speechiness, valence, numberOfSections])

    return listOfID

def getAlbumGenres(albumID, authToken):
    chosenAlbumEndpoint = "{0}/albums/{1}".format(apiURL,albumID)
    getRequest = requests.get(chosenAlbumEndpoint, headers=authToken)

    albumItems = json.loads(getRequest.text)
    with open('album.json', 'w') as outfile:
        json.dump(albumItems, outfile)
    firstGenre = albumItems['genres']
    if len(firstGenre)>0:
        firstGenre = firstGenre[0]
    else:
        firstGenre = 'None'
    return firstGenre

#TODO wykrywanie kodów odpowiedzi Serwera i reagowanie na błędy
#TODO zamień flask na urllib