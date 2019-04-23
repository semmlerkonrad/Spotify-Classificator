# Spotify-Classificator
The aim of this project is to classify song's genre based on its audio data. I got audio data from the Spotify API, which allows to access results of low-level audio analysis performed by it's system on (almost) each of their 30 000 000 songs.
After getting all the atributes, I fitted them into some classifier models available in scikit-learn.

The project directory consists of:
1. trackdigger.py - has methods to connect to Spotify API, download track data, genre info and to return attributes of audio data necessary for the classification process.
2. main.py - manages writing data to CSV, declares how many songs to download and from which genres.
3. DataAnalysis.ipynb - Jupyter Notebook explaining the process of finding the best classification model for the audio data.

In this project I used requests, pandas, scikit-learn, matplotlib and numby library.