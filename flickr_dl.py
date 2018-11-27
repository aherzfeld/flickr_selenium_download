#! /usr/bin/env python3
# flickr_dl.py - downloads photos from flickr using selenium
# usage - flickr_dl.py <search term> <number of photos to dl>

import os
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# TODO: get user arg strings for category and number to dl
search_term = sys.argv[1]
num_to_dl = int(sys.argv[2])
print('Searching "{}" on Flickr and downloading {} images.'.format(
      search_term, num_to_dl))

# TODO: instantiate driver and get website
driver = webdriver.Firefox()
driver.get('https://www.flickr.com/')

# TODO: find search element , input category & submit
search_elem = driver.find_element_by_id('search-field')
search_elem.send_keys(search_term)
search_elem.send_keys(Keys.RETURN)

# TODO: find and click first photo element
photo_elem = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.overlay'))
)
photo_elem.click()

# TODO: create folder in working directory
n = 1
path = os.path.join(os.getcwd, search_term + str(n))
print(path)  # for testing
while True:
    if os.path.exists(path):
        n += 1
    else:
        break
print(path)  # for testing
#path = os.path.join(os.getcwd, search_term + str(n))
try:
    os.mkdir(path)
except FileExistsError as e:
    print(e)

# TODO download n photos
# TODO: loop num_to_dl times
print('Trying to download {} photos.'.format(num_to_dl))
dl_elem = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'download '))
)
dl_elem.click()
# choose size from menu
dl_elem = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'Square'))
)
dl_elem.click()
# TODO: change default firefox settings to avoid dl popup



# TODO: close driver 
driver.close()

