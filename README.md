# Spotify-Classificator
by Konrad Semmler

A project involving digging the audio data of the songs avalaible in the Spotify library and trying to classify their genre based on said data. 

The project directory consists of:
1. trackdigger.py - has methods to connect to Spotify API, download track data, genre info and to return attributes of audio data necessary for the classification process.
2. maindiggingscript.py - manages writing data to CSV, declares how many songs to download and from which genres.

In this project I used requests, pandas, scikit-learn, matplotlib and numby library.
