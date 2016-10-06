from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys
import pickle
import datetime, os

from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse

from demoslogic.users.models import User

class UserTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox(firefox_binary=FirefoxBinary(
            firefox_path='C:\\Program Files\\Mozilla FirefoxESR\\firefox.exe'))
        self.browser.get(self.live_server_url)
        self.browser.implicitly_wait(1)

    def tearDown(self):
        self.browser.quit()
        # pass

    def test_can_login_and_create_premises_and_view_and_delete_them(self):
        User.objects.create_user(username = 'Alfons', email = 'al@fons.com', password = 'top-secretary')
        self.browser.get(self.live_server_url + '/accounts/login/')
        userfield = self.browser.find_element_by_id("id_login")
        userfield.send_keys("Alfons")
        pwfield = self.browser.find_element_by_id("id_password")
        pwfield.send_keys("top-secretary")
        rememberfield = self.browser.find_element_by_id("id_remember")
        rememberfield.click()
        loginbutton = self.browser.find_element_by_id("loginbutton")
        loginbutton.click()
        self.assertIn('User: Alfons', self.browser.title)
        self.browser.find_element_by_link_text('Premises').click()
        self.browser.find_element_by_class_name('link_new_premise').click()
        self.browser.find_element_by_link_text('With complement').click()
        self.browser.find_element_by_id('id_subject').send_keys('Peacocks')
        self.browser.find_element_by_id('id_predicate').send_keys('are')
        self.browser.find_element_by_id('id_complement').send_keys('scary')
        self.browser.find_element_by_id('new_premise_form').submit()
        self.assertIn('Peacocks', self.browser.title)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Alfons', page_text)
        self.browser.find_element_by_class_name('link_created_by').click()
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Peacocks', page_text)
        self.browser.find_element_by_id('id_premise1').click()
        delete_listitem = self.browser.find_element_by_id('id_delete_premise')
        delete_listitem.click()
        try:
            self.browser.find_element_by_link_text('Peacocks')
            self.fail('Premise could not be deleted (or there is another premise with the same text)!')
        except NoSuchElementException:
            pass
