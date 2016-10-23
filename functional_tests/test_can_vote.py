from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest
from demoslogic.premises.models import Premise

class UserCanVoteTest(FunctionalTest):
    fixtures = ['fixtures\\testset.yaml']

    def test_can_vote(self):
        new_premise = Premise(user=self.user, subject="Things", predicate="exist")
        new_premise.save()
        self.browser.find_element_by_link_text('Premises').click()
        self.browser.find_element_by_link_text('Things exist').click()
        self.browser.find_element_by_class_name('radio').click()
        self.browser.find_element_by_tag_name('form').submit()
