import unittest
#import flickr_dl  # have to import the module you're testing
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestFlickrSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    @unittest.SkipTest  # until I sort out the second test class
    def test_search_for_something(self):
        driver = self.driver
        # TODO: test_get_website
        driver.get('https://www.flickr.com/')
        assert driver.current_url == 'https://www.flickr.com/'
        self.assertIn("Flickr", driver.title)
        # TODO: test_find_element
        search_elem = driver.find_element_by_id('search-field')
        # TODO: test_input_category
        search_elem.send_keys('robot')
        # TODO: test_submit
        search_elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source

    def tearDown(self):
        self.driver.close()


# TODO: second unittest: photo results page
class TestFindPhotos(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    # TODO: test_find_photos
    def test_find_photos(self):
        driver = self.driver
        driver.get('https://www.flickr.com/search/?text=robots')
        # find all photos on the page
        photo_elem = driver.find_element_by_css_selector('a.overlay')
        self.assertIsNotNone(photo_elem, "The element was not found.")
        # click the picture link
        photo_elem.click()
        assert 'photos' in driver.current_url
        dl_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'download '))
        )
        dl_elem.click()
        # choose size from menu
        dl_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'Square'))
        )
        dl_elem.click()
        # TODO: prevent firefox window from popping up

        
        elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'navigate-next'))
        )
        elem.click()

    # def tearDown(self):
    #     self.driver.close()

    
    # TODO: test_mkdir


    # TODO: test_dl_images


# allows us to run from command line using: $ python test_flickr.py
if __name__ == '__main__':
    unittest.main()
