# the program is written to log you in; into multiple websites
# the url along with the username and password is suppose to be mentioned in a txt file separated by commas
# the program will read every line and render to the url and log you with your credentials
# the status is printed on console to view faulty url or some issue

# importing all the required modules

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from prettytable import PrettyTable
from bs4 import BeautifulSoup
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager


# getting the latest webdriver for you browser
# (if already have the latest then use it)
driver = webdriver.Chrome(ChromeDriverManager().install())


# reading the file
data = []
file = "songs.txt"
with open(file, 'r') as main_file:
    for line in main_file:
        data.append(line.strip("\n"))

def downlaod_file(link, download_format, open_new_tab = False):
    # format 1 -> mp3
    # format 2 -> mp4 video
    global driver

    tab_index = 1
    url = "https://yt1s.com/en424/youtube-to-mp3" if download_format == 1 else "https://yt1s.com/en424/youtube-to-mp4"
    if open_new_tab:
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[tab_index])
        tab_index += 1
    driver.get(url)
    input_box = driver.find_element("id", "s_input")
    input_box.send_keys(link)
    input_box.send_keys(Keys.ENTER)
    sleep(3)
    get_link = driver.find_element("id", "btn-action")
    get_link.send_keys(Keys.ENTER)
    sleep(2)
    download_button = driver.find_element("id", "asuccess")
    download_button.send_keys(Keys.ENTER)
    sleep(2)

# iterating over the urls in the read txt file
for link in data:
    downlaod_file(link, 1, False)

# closing the browser if all the link are done redirecting
# sleep(5)
# driver.quit()
