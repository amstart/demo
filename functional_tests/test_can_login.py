from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys

from demoslogic.users.models import User
from .base import FunctionalTest

class UserCanLoginTest(FunctionalTest):

    def test_can_login(self):
        User.objects.create_user(username = 'Alfons', email = 'al@fons.com', password = 'top-secretary')
        self.browser.find_element_by_link_text("Sign In").click()
        userfield = self.browser.find_element_by_id("id_login")
        userfield.send_keys("Alfons")
        pwfield = self.browser.find_element_by_id("id_password")
        pwfield.send_keys("top-secretary")
        rememberfield = self.browser.find_element_by_id("id_remember")
        rememberfield.click()
        loginbutton = self.browser.find_element_by_id("loginbutton")
        loginbutton.click()
        self.assertIn('User: Alfons', self.browser.title)
