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
file = "C:\\Users\\anils\\Downloads\\test.txt"
main_file = open(file, 'r')
for line in main_file:
    data.append(line.split(','))
main_file.close()


# using web-scraping to automatically get the form details
# find form with 'post' method -> find all input tags -> get the input with 'type=input' -> store its name/id
def get_login_fields(page):
    login_fields = {}
    soup = BeautifulSoup(page, features='html.parser')
    login_form = soup.find("form", attrs={'method': 'post'})
    if login_form:
        input_tag = login_form.find_all('input')
        text_fields = []
        for tag in input_tag:
            if tag.get('type') == 'hidden':
                continue
            text_fields.append(tag)

        try:
            try:
                login_fields['username'] = text_fields[0].get('name')
                login_fields['password'] = text_fields[1].get('name')
                login_fields['type'] = 'name'
            except:
                login_fields['username'] = text_fields[0].get('id')
                login_fields['password'] = text_fields[1].get('id')
                login_fields['type'] = 'id'
        except:
            print('something went wrong in username/password')
            return None
    else:
        print('No login form found!!!!')
        return None
    return login_fields


# selenium core function that automates the login
# redirects to the url
# insert username and password and loggs in
# requests module is used to get the status of the url back
def make_login(url, user, pass_word):
    global driver, open_new_tab, tab_index
    if open_new_tab:
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[tab_index])
        tab_index += 1
    driver.get(url)
    current_title = driver.title
    r = requests.get(url)
    status_before_login = r.status_code

    web_page = driver.page_source
    login_field = get_login_fields(web_page)

    if login_field is not None:
        sleep(2)
        if login_field['type'] == 'id':
            login_box = driver.find_element_by_id(login_field['username'])
            password_box = driver.find_element_by_id(login_field['password'])
            login_box.send_keys(user)
            password_box.send_keys(pass_word)
            sleep(2)
            try:
                password_box.send_keys(Keys.ENTER)
            except:
                pass
        else:
            login_box = driver.find_element_by_name(login_field['username'])
            password_box = driver.find_element_by_name(login_field['password'])
            login_box.send_keys(user)
            password_box.send_keys(pass_word)
            sleep(2)
            try:
                password_box.send_keys(Keys.ENTER)
            except:
                pass
        sleep(5)
        open_new_tab = True
        status_after_login = "Unknown"
        new_url = driver.current_url
        new_title = current_title

        # checking change in title or url
        # to detect weather login is successfull
        if (url != new_url) or (driver.title != new_title):
            r = requests.get(driver.current_url)
            status_after_login = r.status_code
        x = PrettyTable(["URL", "STATUS BEFORE", "STATUS AFTER"])
        x.add_row([url, status_before_login, status_after_login])
        print(x)
    else:
        print(f'Something went wrong for {url}')


open_new_tab = False
tab_index = 1
# iterating over the urls in the read txt file
for records in data:
    link, username, password = records
    make_login(link, str(username), str(password))


# closing the browser if all the link are done redirecting
sleep(5)
driver.quit()