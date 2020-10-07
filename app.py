from flask import Flask, render_template, request, Response
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="your api id",
                                                           client_secret="your client secret"))


app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def main():
    songs = []
    error=False
    if request.method=="GET":
        return render_template("index.html")
    elif request.method=="POST":
        song_name = request.form["music"].lower()
        results = sp.search(q=song_name, type="track", limit=1)
        if len(results["tracks"]["items"]) == 0:
            error=True
        else:
            id_song = results['tracks']['items'][0]['id']
            name_song = results["tracks"]["items"][0]["external_urls"]["spotify"]
            print("id song ", name_song)
            songs = sp.recommendations(seed_tracks=[id_song],limit=20)["tracks"]
            if(len(songs) == 0):
                error = True
            
        return render_template('index.html', songs=songs, length=len(songs), error=error, music=results['tracks']['items'][0])




if __name__ == "__main__":
    app.run(debug=True)