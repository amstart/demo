from .base import FunctionalTest

class UserCanVoteTest(FunctionalTest):
    fixtures = ['fixtures\\testset.yaml']

    def test_can_vote(self):
        self.create_pre_authenticated_session("Alfons")
        self.browser.find_element_by_link_text('Statements').click()
        self.browser.find_element_by_link_text('This premise is from Gertrud').click()
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Gertrud', page_text)
        self.assertNotIn('edit', page_text)
        self.browser.find_element_by_id('id_value_1').click()
        self.browser.find_element_by_tag_name('form').submit()
        self.assertGreater(self.browser.find_element_by_id('id_choice1').size['width'],
                       self.browser.find_element_by_id('id_choice2').size['width'])
        self.assertEqual(self.browser.find_element_by_id('id_choice2').size['width'],
                       self.browser.find_element_by_id('id_choice3').size['width'])
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('This premise', page_text)
        self.assertIn('(you)', page_text)
        self.assertIn(':', page_text)
        self.assertIn('1', page_text)
        self.browser.find_element_by_link_text('edit vote').click()
        self.browser.find_element_by_id('id_value_4').click()
        self.browser.find_element_by_tag_name('form').submit()
        self.assertIn('This premise', page_text)
        self.assertGreater(self.browser.find_element_by_id('id_choice4').size['width'],
                       self.browser.find_element_by_id('id_choice3').size['width'])
        self.assertEqual(self.browser.find_element_by_id('id_choice1').size['width'],
                       self.browser.find_element_by_id('id_choice2').size['width'])
