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

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)
