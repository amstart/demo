from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import os

from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from demoslogic.users.models import User

def create_pre_authenticated_session(browser, live_server_url):
    if browser.capabilities['browserName'] == 'phantomjs':
        browser.get(live_server_url + "/accounts/login/")
        browser.find_element_by_id("id_login").send_keys("Alfons")
        browser.find_element_by_id("id_password").send_keys("top-secretary")
        browser.find_element_by_tag_name("form").submit()
        browser.implicitly_wait(0.5)
    else:
        session = SessionStore()
        users = User.objects.all()
        session[SESSION_KEY] = users[0].pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()
        ## to set a cookie we need to first visit the domain.
        ## 404 pages load the quickest!
        browser.get(live_server_url)
        browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session.session_key,
            path='/',
        ))
    browser.get(live_server_url + "/selenium/")
    return browser

class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        super(FunctionalTest, self).setUp()
        self.browser = webdriver.Chrome(executable_path = "C:\\Tools\\chromedriver\\chromedriver.exe")
        # self.browser = webdriver.Firefox(firefox_binary=FirefoxBinary(
        #     firefox_path='C:\\Program Files\\Mozilla FirefoxESR\\firefox.exe'))
        self.browser.set_page_load_timeout(10)
        self.browser.set_script_timeout(10)

    def tearDown(self):
        self.browser.quit()
        super(FunctionalTest, self).tearDown()
        pass

    def create_pre_authenticated_session(self, name):
        create_pre_authenticated_session(self.browser, self.live_server_url)
