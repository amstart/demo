from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys
import pickle
import datetime, os

from django.test import LiveServerTestCase

from demoslogic.users.models import User

class UserTest(LiveServerTestCase):
    def setUp(self):
        User.objects.create_user(username = 'Alfons', email = 'al@fons.com', password = 'top-secretary')
        self.browser = webdriver.Firefox(firefox_binary=FirefoxBinary(
            firefox_path='C:\\Program Files\\Mozilla FirefoxESR\\firefox.exe'))
        self.browser.get(self.live_server_url)
        self.browser.implicitly_wait(1)

        # This logs in and generates a cookie (if the cookie is older than 5 days)
        file_modified = datetime.datetime.fromtimestamp(os.path.getmtime("test_cookies.pkl"))
        if datetime.datetime.now() - file_modified < datetime.timedelta(days=5):
            self.browser.get(self.live_server_url + '/accounts/login/')
            userfield = self.browser.find_element_by_id("id_login")
            userfield.send_keys("Alfons")
            pwfield = self.browser.find_element_by_id("id_password")
            pwfield.send_keys("top-secretary")
            rememberfield = self.browser.find_element_by_id("id_remember")
            rememberfield.click()
            loginbutton = self.browser.find_element_by_id("loginbutton")
            loginbutton.click()
            # She notices the page title and header mention to-do lists
            self.assertIn('User: Alfons', self.browser.title)
            pickle.dump( self.browser.get_cookies() , open("test_cookies.pkl","wb"))
        else:
            cookies = pickle.load(open("test_cookies.pkl", "rb"))
            for cookie in cookies:
                self.browser.add_cookie(cookie)

    def tearDown(self):
        #pass
        self.browser.quit()

    def test_can_create_premises_and_view_and_delete_them(self):
        self.browser.find_element_by_link_text('Premises').click()
        self.browser.find_element_by_class_name('link-new-premise').click()
        self.browser.find_element_by_link_text('With complement').click()
        # self.browser.get(self.live_server_url +'/premises/new/min')
        inputbox = self.browser.find_element_by_id('id_subject')
        # self.assertEqual(
        #         inputbox.get_attribute('placeholder'),
        #         'subject'
        # )
        premise_subject = 'Peacocks'
        inputbox.send_keys(premise_subject)
        self.browser.find_element_by_id('id_predicate').send_keys('are')
        self.browser.find_element_by_id('id_complement').send_keys('scary')
        self.browser.find_element_by_id('new_premise_form').submit()
        #detail page about new premise
        self.assertIn(premise_subject, self.browser.title)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Alfons', page_text)
        delete_listitem = self.browser.find_element_by_id('id_delete_premise')
        delete_listitem.click()
        try:
            self.browser.find_element_by_link_text(premise_subject)
            self.fail('Premise could not be deleted (or there is another premise with the same text)!')
        except NoSuchElementException:
            pass
        self.fail('Finish the test!')
