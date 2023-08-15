from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

# Function to retrieve data from the database
def get_song_history():
    conn = sqlite3.connect('song_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM song_history")
    songs = cursor.fetchall()
    conn.close()
    return songs

@app.route('/')
def index():
    songs = get_song_history()
    return render_template('index.html', songs=songs)

# Route to retrieve refreshed song data
@app.route('/refresh')
def refresh_song_data():
    songs = get_song_history()
    
    if songs:
        currently_playing = f"<div class='currently-playing'>Currently playing:<br>{songs[-1][1]} by {songs[-1][2]}</div>"
        song_history_rows = ""
        for song in reversed(songs[:-1]):
            song_history_rows += f"<tr><td>{song[1]}</td><td>{song[2]}</td><td>{song[3]}</td></tr>"
        response_data = f"{currently_playing}<!-- SPLIT -->{song_history_rows}"
    else:
        response_data = "No song history available."

    return response_data

if __name__ == '__main__':
    app.run(debug=True)