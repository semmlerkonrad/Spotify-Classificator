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

    #zapisujemy do pliku json na wszelki wypadek i potem zwracamy do funkcji, żeby przetworzyć
    with open('DANGERZONE.json', 'w') as outfile:
        json.dump(analysisData, outfile)
    return analysisData


def getTrackIDsFromPlaylist(playlistID, authToken):
    chosenPlaylistEndpoint = "{0}/playlists/{1}/tracks".format(apiURL, playlistID)
    getRequest = requests.get(chosenPlaylistEndpoint, headers=authToken)

    tracksData = json.loads(getRequest.text)
    with open('tracks.json', 'w') as outfile:
        json.dump(tracksData, outfile)
    return tracksData
