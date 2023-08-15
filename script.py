from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import sqlite3

# Initialize the SQLite database and create a table
conn = sqlite3.connect('song_data.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS song_history
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   song TEXT,
                   artist TEXT,
                   timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
conn.commit()

options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome(options)

driver.get("https://www.siriusxm.com/channels/bpm")

previous_song = None

clock = 0
# Run for 10 minutes
while clock != 600:
    song_elements = driver.find_elements(By.XPATH, "//div[@class='card-spotlight--now-playing--song']/span")
    artist_elements = driver.find_elements(By.XPATH, "//div[@class='card-spotlight--now-playing--artist']/span")
    
    if song_elements and artist_elements:
        current_song = song_elements[1].text
        current_artist = artist_elements[1].text
        
        if current_song != previous_song:
            
            # Insert data into the database
            cursor.execute("INSERT INTO song_history (song, artist) VALUES (?, ?)", (current_song, current_artist))
            conn.commit()
            
            previous_song = current_song
        
    time.sleep(10)
    clock += 10

driver.quit()

# Close the database connection
conn.close()
