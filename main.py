from flask import Flask, json, redirect
import getData
app = Flask(__name__)

@app.route("/")
def index():
    return redirect(getData.redirectURI)

@app.route("/callback/q")
def callback():

    authToken = getData.getAuthToken()

    #analiza audio DANGER ZONE
    DANGERZONE = getData.getAudioAnalysis('34x6hEJgGAOQvmlMql5Ige', authToken)

    myPlaylistTracks = getData.getTrackIDsFromPlaylist('5N13fntbZVqW2euiBTfbD2', authToken)
    #zwracamy plik json to przeglądarki
    return json.dumps(myPlaylistTracks)


if __name__ == "__main__":
    # po włączeniu wchodzimy na "http://127.0.0.1:8080" żeby wykonać zapytania zapisane w callback()
    app.run(debug=True,port=8080)