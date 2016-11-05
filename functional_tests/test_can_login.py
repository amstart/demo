from .base import FunctionalTest

class UserCanLoginTest(FunctionalTest):
    fixtures = ['fixtures\\testset.yaml']

    def test_can_login(self):
        self.browser.find_element_by_link_text("Sign In").click()
        userfield = self.browser.find_element_by_id("id_login")
        userfield.send_keys("Alfons")
        pwfield = self.browser.find_element_by_id("id_password")
        pwfield.send_keys("top-secretary")
        rememberfield = self.browser.find_element_by_id("id_remember")
        rememberfield.click()
        self.browser.find_element_by_tag_name("form").submit()
        # loginbutton.click()
        self.assertIn('User: Alfons', self.browser.title)
