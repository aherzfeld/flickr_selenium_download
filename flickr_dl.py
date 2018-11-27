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
from selenium.common.exceptions import TimeoutException


# TODO: get user arg strings for category and number to dl
search_term = sys.argv[1]
num_to_dl = int(sys.argv[2])
print('Searching "{}" on Flickr and downloading {} images.'.format(
      search_term, num_to_dl))

# TODO: instantiate driver and get website + search
driver = webdriver.Firefox()
driver.get('https://www.flickr.com/search/?text=' + search_term)

# TODO: find and click first photo element
try:
    photo_elem = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'a.overlay'))
    )
except TimeoutException:
    photo_elem = driver.find_element_by_css_selector('a.overlay')
    print('Timeout Exception was raised')
photo_elem.click()

# TODO: create folder in working directory
n = 1
while True:
    file_name = search_term + str(n)
    if not os.path.exists(os.path.join(os.getcwd(), file_name)):
        break
    n += 1

path = os.path.join(os.getcwd(), file_name)
try:
    os.mkdir(path)
    print('Created {} directory.'.format(os.path.basename(path)))
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

