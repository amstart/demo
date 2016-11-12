from selenium.common.exceptions import NoSuchElementException
from demoslogic.premises.models import Premise

from .base import FunctionalTest

class UserTest(FunctionalTest):
    fixtures = ['fixtures\\testset.yaml']

    def test_create_arguments_form(self):
        # print('This is what the test sees:' + str(Premise.objects.all()))
        self.create_pre_authenticated_session("Alfons")
        self.browser.find_element_by_link_text('Arguments').click()
        self.browser.find_element_by_class_name('new_object').click()
        self.browser.find_element_by_css_selector('#id_premise1 + span').click()
        self.browser.find_element_by_class_name('select2-search__field').send_keys('This premise is from Alfons')
        self.browser.find_element_by_css_selector('#id_premise2 + span')
        self.browser.find_element_by_css_selector('#id_conclusion + span')
        # self.browser.implicitly_wait(0.5)
        # # subContainerClass = '#select2-drop:not([style*='display: none'])'
        # # self.browser.wait.Until(self.browser.ExpectedConditions.ElementIsVisible(
        # #     self.browser.find_element_by_link_text("This premise is from Alfons")))
        # self.browser.implicitly_wait(0.5)
        # self.browser.find_element_by_css_selector('.select2-dropdown:not([style*=\'display: none\']) li').click()
        # self.browser.implicitly_wait(10)
        # self.browser
        # self.browser.find_element_by_id('id_premise2').send_keys('This premise is from Gertrud')
        # self.browser.find_element_by_id('id_conclusion').send_keys('This premise has been voted on')
        # self.browser.find_element_by_id('new_argument_form').submit()
        # self.assertIn('Pro: This premise has been voted on', self.browser.title)
        # page_text = self.browser.find_element_by_tag_name('body').text
        # self.assertIn('Pro: This premise has been voted on', page_text)
        # self.browser.find_element_by_class_name('link_created_by').click()
        # page_text = self.browser.find_element_by_tag_name('body').text
        # self.assertIn('created 2 premise and 3 arguments', page_text)
        # self.browser.find_element_by_link_text('Arguments').click()
        # self.browser.find_element_by_id('id_argument4').click()
        # self.browser.find_element_by_id('id_delete').click()
        # self.browser.find_element_by_tag_name('form').submit()
        # try:
        #     self.browser.find_element_by_id('id_argument4')
        #     self.fail('Premise could not be deleted (or there is another premise with the same text)!')
        # except NoSuchElementException:
        #     pass
