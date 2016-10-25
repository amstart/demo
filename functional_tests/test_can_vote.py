from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest
from demoslogic.premises.models import Premise

class UserCanVoteTest(FunctionalTest):
    fixtures = ['fixtures\\testset.yaml']

    def test_can_vote(self):
        self.create_pre_authenticated_session("Alfons")
        self.browser.find_element_by_link_text('Premises').click()
        self.browser.find_element_by_link_text('This premise is from Gertrud').click()
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('You have already voted!', page_text)
        self.browser.find_element_by_id('id_value_1').click()
        self.browser.find_element_by_tag_name('form').submit()
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('This premise', page_text)
        self.assertIn('You have already voted!', page_text)
