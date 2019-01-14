import json
import requests
import base64
import urllib

# Client Keys
CLIENT_ID = input()
CLIENT_SECRET = input()

#Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_URL = "https://api.spotify.com/v1"

#Server-side Parameters
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 8080
REDIRECT_URI = "{}:{}/callback/q".format(CLIENT_SIDE_URL, PORT)
SCOPE = "user-library-read"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

#Authorization of application with Spotify
def app_Authorization():
    auth_query_parameters = {
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
        "state": STATE,
        "show_dialog": SHOW_DIALOG_str,
        "client_id": CLIENT_ID
    }
    url_args = "&".join(["{}={}".format(key,urllib.parse.quote(val)) for key,val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return auth_url

#User allows us to access there spotify
def user_Authorization():
    #auth_token = request.args['code']
    code_payload = {"grant_type": "client_credentials"}
    string_bytes = "{}:{}".format(CLIENT_ID, CLIENT_SECRET).encode("ascii")
    base64encoded = base64.b64encode(string_bytes)
    headers = {"Authorization": "Basic {}".format(base64encoded.decode('ascii'))}
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)

    # Tokens are Returned to Application
    response_data = json.loads(post_request.text)
    with open('response.json', 'w') as outfile:
        json.dump(response_data, outfile)

    access_token = response_data["access_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]

    # Use the access token to access Spotify API
    authorization_header = {"Authorization":"Bearer {}".format(access_token)}
    return authorization_header

#Gathering of profile information
def Profile_Data(header):
    # Get user profile data
    user_profile_api_endpoint = "{}/me".format(SPOTIFY_API_URL)
    profile_response = requests.get(user_profile_api_endpoint, headers=header)
    profile_data = json.loads(profile_response.text)
    return profile_data

#Gathering of playlist information
def Playlist_Data(header,profile):
    # Get user playlist data
    playlist_api_endpoint = "{}/playlists".format(profile["href"])
    playlists_response = requests.get(playlist_api_endpoint, headers=header)
    playlist_data = json.loads(playlists_response.text)
    return playlist_data

#Gathering of album information
def Album_Data(header,profile,limit,offset):
    # Get user albums data
    artist_api_endpoint = ("{}/albums?limit=" + str(limit) + "&offset=" + str(offset)).format(profile["href"])
    artist_response = requests.get(artist_api_endpoint, headers=header)
    artist_data = json.loads(artist_response.text)
    return artist_data

def getAudioAnalysis(trackId, authToken):
    chosenTrackEndpoint = "{0}/audio-analysis/{1}".format(SPOTIFY_API_URL, trackId)
    #authHeader = {"Authorization": "Bearer {}".format(authToken)}

    getRequest  = requests.get(chosenTrackEndpoint, headers = authToken)
    analysisData = json.loads(getRequest.text)
    with open('DANGERZONE.json', 'w') as outfile:
        json.dump(analysisData, outfile)
    return analysisData


