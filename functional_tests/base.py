from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from demoslogic.users.models import User

class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        super(FunctionalTest, self).setUp()
        users = User.objects.all()
        if users:
            self.user = users[0]
        self.browser = webdriver.Firefox(firefox_binary=FirefoxBinary(
            firefox_path='C:\\Program Files\\Mozilla FirefoxESR\\firefox.exe'))
        self.browser.get(self.live_server_url)
        self.browser.implicitly_wait(0.5)

    def tearDown(self):
        self.browser.quit()
        super(FunctionalTest, self).tearDown()
        pass

    def create_pre_authenticated_session(self, name):
        session = SessionStore()
        session[SESSION_KEY] = self.user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()
        ## to set a cookie we need to first visit the domain.
        ## 404 pages load the quickest!
        self.browser.get(self.live_server_url)
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session.session_key,
            path='/',
        ))
        self.browser.get(self.live_server_url + "/selenium/")
