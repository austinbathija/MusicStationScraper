from selenium import webdriver
from selenium.webdriver.common.by import By
import time

options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome(options)

driver.get("https://www.siriusxm.com/channels/bpm")

previous_song = None

while True:
    # Find the elements matching the XPath for song and artist
    song_elements = driver.find_elements(By.XPATH, "//div[@class='card-spotlight--now-playing--song']/span")
    artist_elements = driver.find_elements(By.XPATH, "//div[@class='card-spotlight--now-playing--artist']/span")
    
    if song_elements and artist_elements:
        current_song = song_elements[1].text
        current_artist = artist_elements[1].text
        
        if current_song != previous_song:
            print("Song:", current_song)
            print("Artist:", current_artist)
            previous_song = current_song
        
    time.sleep(10)  # Wait for 10 seconds before checking again

driver.quit()
