from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys
import pickle
import unittest
import datetime, os


class UserTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox(firefox_binary=FirefoxBinary(
            firefox_path='C:\\Program Files\\Mozilla FirefoxESR\\firefox.exe'))
        self.browser.get('http://localhost:8000/')
        self.browser.implicitly_wait(1)

        # This logs in and generates a cookie (if the cookie is older than 5 days)
        file_modified = datetime.datetime.fromtimestamp(os.path.getmtime("test_cookies.pkl"))
        if datetime.datetime.now() - file_modified > datetime.timedelta(days=5):
            self.browser.get('http://localhost:8000/accounts/login/')
            userfield = self.browser.find_element_by_id("id_login")
            userfield.send_keys("Jochen")
            pwfield = self.browser.find_element_by_id("id_password")
            pwfield.send_keys("b83cfg")
            rememberfield = self.browser.find_element_by_id("id_remember")
            rememberfield.click()
            loginbutton = self.browser.find_element_by_id("loginbutton")
            loginbutton.click()
            # She notices the page title and header mention to-do lists
            self.assertIn('User: Jochen', self.browser.title)
            pickle.dump( self.browser.get_cookies() , open("test_cookies.pkl","wb"))
        else:
            cookies = pickle.load(open("test_cookies.pkl", "rb"))
            for cookie in cookies:
                self.browser.add_cookie(cookie)

    def tearDown(self):
        #pass
        self.browser.quit()

    def test_can_create_premises_and_view_and_delete_them(self):
        self.browser.get('http://localhost:8000/premises/')
        inputbox = self.browser.find_element_by_id('id_new_premise')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter a premise'
        )
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        listitem = self.browser.find_element_by_id('id_premise1')
        listitem.click()
        #detail page about new premise
        self.assertIn('premise_name', self.browser.title)
        listitem = self.browser.find_element_by_id('id_premise1')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Buy peacock feathers' for row in rows)
        )
        self.fail('Finish the test!')

if __name__ == '__main__':
    unittest.main(warnings='ignore')
