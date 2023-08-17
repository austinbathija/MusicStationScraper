from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import sqlite3

# Initialize the SQLite database and create a table
conn = sqlite3.connect('MultiStation_SongData.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS song_history
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   station TEXT,
                   song TEXT,
                   artist TEXT,
                   times_played INTEGER DEFAULT 1,
                   timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
conn.commit()

options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome(options=options)

# Define station names and URLs
station_urls = [
    ("A State of Armin", "https://www.siriusxm.com/channels/a-state-of-armin"),
    ("BPM", "https://www.siriusxm.com/channels/bpm"),
    ("Chill", "https://www.siriusxm.com/channels/chill")
]

previous_songs = {}

clock = 0

# Run for 1200 minutes to get 1200 songs
while clock != 72000:
    for station_name, url in station_urls:
        driver.get(url)
        song_elements = driver.find_elements(By.XPATH, "//div[@class='card-spotlight--now-playing--song']/span")
        artist_elements = driver.find_elements(By.XPATH, "//div[@class='card-spotlight--now-playing--artist']/span")

        if song_elements and artist_elements:
            current_song = song_elements[1].text
            current_artist = artist_elements[1].text

            key = f"{station_name}_{current_song}_{current_artist}"
            if key not in previous_songs:
                cursor.execute("SELECT times_played FROM song_history WHERE song = ? AND artist = ?", (current_song, current_artist))
                existing_entry = cursor.fetchone()

                if existing_entry:
                    times_played = existing_entry[0]
                    cursor.execute("INSERT INTO song_history (station, song, artist, times_played) VALUES (?, ?, ?, ?)", (station_name, current_song, current_artist, times_played + 1))
                else:
                    cursor.execute("INSERT INTO song_history (station, song, artist) VALUES (?, ?, ?)", (station_name, current_song, current_artist))

                conn.commit()

            previous_songs[key] = True

        time.sleep(10)

    clock += 10

# Close the driver
driver.quit()

# Close the database connection
conn.close()
