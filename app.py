from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

def get_song_history():
    conn = sqlite3.connect('MultiStation_SongData.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM song_history")
    songs = cursor.fetchall()
    conn.close()
    return songs

@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/landingpage')
def landing_page():
    return render_template('landing.html')

@app.route('/bpm')
def bpm():
    return render_template('bpm.html')

@app.route('/chill')
def chill():
    return render_template('chill.html')

@app.route('/armin')
def armin():
    return render_template('armin.html')

@app.route('/refresh/bpm')
def refresh_bpm_song_data():
    songs = get_song_history()

    bpm_songs = [song for song in songs if song[1] == "BPM"]

    now_playing = ""
    song_history_rows = ""
    if bpm_songs:
        latest_song = bpm_songs[-1]  # Get the latest song
        now_playing = f"<div class='currently-playing'>{latest_song[2]} - {latest_song[3]}</div>"

        # Exclude the latest song from the history
        history_songs = bpm_songs[:-1]
        for song in reversed(history_songs):
            song_history_rows += f"<tr><td>{song[2]}</td><td>{song[3]}</td><td>{song[4]}</td><td>{song[5]}</td></tr>"
    else:
        song_history_rows = "<tr><td colspan='3'>No song history available for BPM station.</td></tr>"

    return now_playing + "<!--SPLIT-->" + song_history_rows


@app.route('/refresh/chill')
def refresh_chill_song_data():
    songs = get_song_history()

    chill_songs = [song for song in songs if song[1] == "Chill"]

    now_playing = ""
    song_history_rows = ""
    if chill_songs:
        latest_song = chill_songs[-1]  # Get the latest song
        now_playing = f"<div class='currently-playing'><span id='song-title'>{latest_song[2]}</span><br><span id='artist'>{latest_song[3]}</span></div>"

        # Exclude the latest song from the history
        history_songs = chill_songs[:-1]
        for song in reversed(history_songs):
            song_history_rows += f"<tr><td>{song[2]}</td><td>{song[3]}</td><td>{song[4]}</td><td>{song[5]}</td></tr>"
    else:
        song_history_rows = "<tr><td colspan='3'>No song history available for Chill station.</td></tr>"

    return now_playing + "<!--SPLIT-->" + song_history_rows


@app.route('/refresh/armin')
def refresh_armin_song_data():
    songs = get_song_history()

    armin_songs = [song for song in songs if song[1] == "A State of Armin"]

    now_playing = ""
    song_history_rows = ""
    if armin_songs:
        latest_song = armin_songs[-1]  # Get the latest song
        now_playing = f"<div class='currently-playing'>{latest_song[2]} - {latest_song[3]}</div>"

        # Exclude the latest song from the history
        history_songs = armin_songs[:-1]
        for song in reversed(history_songs):
            song_history_rows += f"<tr><td>{song[2]}</td><td>{song[3]}</td><td>{song[4]}</td><td>{song[5]}</td></tr>"
    else:
        song_history_rows = "<tr><td colspan='3'>No song history available for Armin station.</td></tr>"

    return now_playing + "<!--SPLIT-->" + song_history_rows

if __name__ == '__main__':
    app.run(debug=True)
