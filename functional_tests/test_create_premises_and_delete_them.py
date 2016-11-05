from selenium.common.exceptions import NoSuchElementException

from .base import FunctionalTest

class UserTest(FunctionalTest):
    fixtures = ['fixtures\\testusers.yaml']

    def test_create_premises_and_view_and_delete_them(self):
        self.create_pre_authenticated_session("Alfons")
        self.browser.find_element_by_link_text('Premises').click()
        self.browser.find_element_by_class_name('link_new_premise').click()
        self.browser.find_element_by_link_text('With complement').click()
        self.browser.find_element_by_id('id_subject').send_keys('Peacocks')
        self.browser.find_element_by_id('id_predicate').send_keys('are')
        self.browser.find_element_by_id('id_complement').send_keys('scary')
        self.browser.find_element_by_id('new_premise_form').submit()
        self.assertIn('Peacocks', self.browser.title)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.browser.find_element_by_class_name('link_created_by').click()
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('created 1 premise and 0 arguments', page_text)
        self.browser.find_element_by_link_text('Premises').click()
        self.browser.find_element_by_id('id_premise1').click()
        self.browser.find_element_by_id('id_delete').click()
        self.browser.find_element_by_tag_name('form').submit()
        try:
            self.browser.find_element_by_id('id_premise1')
            self.fail('Premise could not be deleted (or there is another premise with the same text)!')
        except NoSuchElementException:
            pass