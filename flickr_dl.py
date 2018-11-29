#! /usr/bin/env python3
# flickr_dl.py - downloads photos from flickr using selenium
# usage - flickr_dl.py <search term> <number of photos to dl>

import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.firefox.options import Options


#TODO: add input verification
# get user arg strings for category and number to dl
search_term = sys.argv[1]
num_to_dl = int(sys.argv[2])
print('Searching "{}" on Flickr and downloading {} images.'.format(
      search_term, num_to_dl))

# create folder in working directory
n = 1
while True:
    dir_name = search_term + str(n)
    if not os.path.exists(os.path.join(os.getcwd(), dir_name)):
        break
    n += 1

path = os.path.join(os.getcwd(), dir_name)
try:
    os.mkdir(path)
    print('Created {} directory.'.format(os.path.basename(path)))
except FileExistsError as e:
    print(e)

# TODO: instantiate driver and adjust firefox settings to avoid dl popup
options = Options()
options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.download.manager.showWhenStarting", False)
options.set_preference("browser.download.dir", path)
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "image/jpeg")
driver = webdriver.Firefox(options=options)

# get website + search query
driver.get('https://www.flickr.com/search/?text=' + search_term)

# find and click first photo element
try:
    photo_elem = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'a.overlay'))
    )
except TimeoutException:
    photo_elem = driver.find_element_by_css_selector('a.overlay')
    print('Timeout Exception was raised')
photo_elem.click()


# photo download helper functions
def go_to_next_image():
    next_elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'navigate-next'))
    )
    next_elem.send_keys(Keys.RETURN)


def download_image():
    dl_elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'download '))
    )
    try:
        dl_elem.click()
    except StaleElementReferenceException as e:
        print(e)
        dl_elem = driver.find_element_by_class_name('download ')
        dl_elem.click()
    # choose size from menu
    dl_elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'Square'))
    )
    dl_elem.click()


print('Downloading {} photos.'.format(num_to_dl))
# download first image
download_image()
# loop through remaining images
for i in range(num_to_dl - 1):
    # TODO: remove the download options popup
    elem = driver.switch_to.active_element
    elem.send_keys(Keys.ESCAPE)
    go_to_next_image()
    try:
        download_image()
    except:
        go_to_next_image()
        download_image()

# TODO: rename images
image_list = os.listdir(path)
for i in range(1, len(image_list) + 1):
    pass

# close driver
driver.close()
