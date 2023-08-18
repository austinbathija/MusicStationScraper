from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

# Function to retrieve song history from the database
def get_song_history():
    conn = sqlite3.connect('MultiStation_SongData.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM song_history")
    songs = cursor.fetchall()
    conn.close()
    return songs

# Landing page route
@app.route('/')
@app.route('/landingpage')
def landing_page():
    return render_template('landing.html')

# Page routes for each station
@app.route('/bpm')
def bpm():
    return render_template('bpm.html')

@app.route('/chill')
def chill():
    return render_template('chill.html')

@app.route('/armin')
def armin():
    return render_template('armin.html')

# Function to refresh song data for a specific station
def refresh_song_data(station_name):
    songs = get_song_history()
    station_songs = [song for song in songs if song[1] == station_name]

    now_playing = ""
    song_history_rows = ""

    if station_songs:
        latest_song = station_songs[-1]
        now_playing = (
            f"<div class='currently-playing'>"
            f"<span id='song-title'>{latest_song[2]}</span><br>"
            f"<span id='artist'>{latest_song[3]}</span></div>"
        )

        history_songs = station_songs[:-1]
        for song in reversed(history_songs):
            song_history_rows += (
                f"<tr><td>{song[2]}</td><td>{song[3]}</td>"
                f"<td>{song[4]}</td><td>{song[5]}</td></tr>"
            )
    else:
        song_history_rows = (
            f"<tr><td colspan='3'>No song history available for "
            f"{station_name} station.</td></tr>"
        )

    return now_playing + "<!--SPLIT-->" + song_history_rows

# Refresh routes for each station
@app.route('/refresh/bpm')
def refresh_bpm():
    return refresh_song_data("BPM")

@app.route('/refresh/chill')
def refresh_chill():
    return refresh_song_data("Chill")

@app.route('/refresh/armin')
def refresh_armin():
    return refresh_song_data("A State of Armin")

if __name__ == '__main__':
    app.run(debug=True)
