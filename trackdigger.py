import requests
import base64
import time
import numpy as np


class TrackDigger:
    # Spotify URLs for connecting
    spotify_token = "https://accounts.spotify.com/api/token"
    spotify_api = "https://api.spotify.com/v1"

    def __init__(self, client_id, client_secret):
        self._client_id = client_id
        self._client_secret = client_secret
        self._auth_token = ''

    # Authentication token is required for most queries with Spotify API, it is d
    def get_auth_token(self):
        time.sleep(.1)
        body_POST = {"grant_type": "client_credentials"}
        client_id_encoded = "{}:{}".format(self._client_id, self._client_secret).encode("ascii")
        base64_encoded = base64.b64encode(client_id_encoded)
        headers = {"Authorization": "Basic {}".format(base64_encoded.decode('ascii'))}
        POST_request = requests.post(self.spotify_token, data=body_POST, headers=headers)

        # If the answer was not 200, sends the request again after some period of time
        while not POST_request.ok:
            try:
                self.check_error_code(POST_request)
            except TryAgainException:
                print('server error: request {}'.format(self.spotify_token))
                POST_request = requests.post(self.spotify_token, data=body_POST, headers=headers)
                print(POST_request.status_code)

        # Access token is taken from the response and saved in the format specified by the Spotify API
        server_response = POST_request.json()
        access_token = server_response["access_token"]
        self._auth_token = {"Authorization": "Bearer {}".format(access_token)}
        print('Connected to the Spotify Server')

    # Request for the Audio Analysis of the specified track
    def get_audio_analysis(self, track_id):
        time.sleep(.1)
        chosen_track_endpoint = "{0}/audio-analysis/{1}".format(self.spotify_api, track_id)
        get_request = requests.get(chosen_track_endpoint, headers=self._auth_token)

        while not get_request.ok:
            get_request = self.check_for_error(chosen_track_endpoint, get_request)

        analysis_data = get_request.json()
        return analysis_data

    # Request for the Audio Features of the specified track
    def get_audio_features(self, track_id):
        time.sleep(.1)
        chosenTrackEndpoint = "{0}/audio-features/{1}".format(self.spotify_api, track_id)
        getRequest = requests.get(chosenTrackEndpoint, headers=self._auth_token)

        while not getRequest.ok:
            getRequest = self.check_for_error(chosenTrackEndpoint, getRequest)

        analysisData = getRequest.json()
        return analysisData

    # Request for a list of all available genres to use with the recommend songs request
    def get_genres(self):
        time.sleep(.1)
        genres_endpoint = "{0}/recommendations/available-genre-seeds".format(self.spotify_api)
        get_request = requests.get(genres_endpoint, headers=self._auth_token)

        while not get_request.ok:
            get_request = self.check_for_error(genres_endpoint, get_request)

        genre_data = get_request.json()['genres']
        return genre_data

    # Starts checkup of the error code returned by the server to the GET request
    def check_for_error(self, endpoint, get_request):
        try:
            self.check_error_code(get_request)
        except TryAgainException:
            print('server error: request {}'.format(endpoint))
            get_request = requests.get(endpoint, headers=self._auth_token)
            print(get_request.status_code)
        return get_request

    # Downloads all the data from songs of the specified genre and only returns neccesary attributes. First the genre is 
    # feeded to recommendation engine, who then returns 100 songs which fit this requirement. Then it collects Audio Analysis
    # and Audio Feature data for each songs and returns specified attributes.
    def get_tracks_and_their_data(self, genre):
        time.sleep(.1)
        number_of_tracks_downloaded = 100
        tracks_endpoint = "{0}/recommendations?limit={1}&seed_genres={2}".format(self.spotify_api,
                                                                                 number_of_tracks_downloaded, genre)
        get_request = requests.get(tracks_endpoint, headers=self._auth_token)

        while not get_request.ok:
            get_request = self.check_for_error(tracks_endpoint, get_request)

        track_data = []
        tracks_json = get_request.json()['tracks']
        for track in tracks_json:
            track_id = track['id']
            try:
                track_audio_features = self.get_audio_features(track_id)
                track_audio_data = self.get_audio_analysis(track_id)

                end_of_fade_in = track_audio_data['track']['end_of_fade_in']
                start_of_fade_out = track_audio_data['track']['start_of_fade_out']
                loudness = track_audio_data['track']['loudness']
                tempo = track_audio_data['track']['tempo']
                timeSignature = track_audio_data['track']['time_signature']
                mode = track_audio_data['track']['mode']
                key = track_audio_features['key']
                number_of_sections = len(track_audio_data['sections'])

                segments_attack = []
                for segment in track_audio_data["segments"]:
                    loudness_start = segment["loudness_start"]
                    loudness_end = segment["loudness_max"]
                    loudness_end_time = segment["loudness_max_time"]
                    if loudness_end_time == 0 or loudness_end_time is None:
                        attack = 0
                    else:
                        loudness_difference = np.abs(loudness_start - loudness_end)
                        attack = loudness_difference / loudness_end_time
                    segments_attack.append(attack)

                attack_average = np.around(np.nanmean(segments_attack), decimals=3)

                track_data.append([genre, end_of_fade_in, start_of_fade_out, loudness, tempo,
                                   timeSignature, mode, key, number_of_sections, attack_average])
            except NotFoundException:
                print('Skipping track {}, as it does not have analysis data.'.format(track_id))

        return track_data

    # Checks which error code has the server returned
    def check_error_code(self, request):
        
        # Too many requests have been made and you need to wait before making another one
        if request.status_code == 429:
            seconds = request.headers['Retry-After']
            seconds += 3
            print('Too Many Requests: waiting {} seconds.'.format(seconds))
            time.sleep(seconds)
            raise TryAgainException

        # Track has no data
        elif request.status_code == 404:
            raise NotFoundException

        # Authorization token has expired or was invalid and you need to get another one
        elif request.status_code == 401:
            time.sleep(15)
            print('getting new Authentication Token')
            self.get_auth_token()
            raise TryAgainException


class NotFoundException(Exception):
    """Raised when the current track does not have an analysis or features on the Spotify server"""


class TryAgainException(Exception):
    """Raised when the current request has to be submitted again to the server"""
