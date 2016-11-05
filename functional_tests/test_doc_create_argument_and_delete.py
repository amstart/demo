from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import pytest
import os
import django
from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY
from django.contrib.sessions.backends.db import SessionStore
os.environ['DJANGO_SETTINGS_MODULE'] = "config.settings.local"
django.setup()

from demoslogic.users.models import User

pytest.mark.django_db(transaction=False)
browser = webdriver.Firefox(firefox_binary=FirefoxBinary(
    firefox_path='C:\\Program Files\\Mozilla FirefoxESR\\firefox.exe'))
live_server_url = 'http://127.0.0.1:8000'
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
    path=live_server_url,
))
browser.get(live_server_url + "/selenium/")
browser.get(live_server_url + '/arguments/new/create')
browser.implicitly_wait(1)
browser.find_element_by_css_selector('#id_premise1 + span').click()
browser.find_element_by_class_name('select2-search__field').send_keys('This premise')
page_text = browser.find_element_by_tag_name('body').text
assert "This premise is from Alfons" in page_text
css = '#select2-id_premise1-results:first-child'

wait = WebDriverWait(browser, 10)
elm = wait.until(
    EC.element_to_be_clickable(
        (
            By.CSS_SELECTOR,
            css
        )
    ),
    'waiting for %s to be clickable' % (css)
)
elm.click()
browser.find_element_by_tag_name("form").submit()
