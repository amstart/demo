from .base import FunctionalTest

class LayoutTest(FunctionalTest):

    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)
        about_link = self.browser.find_element_by_link_text('About')
        self.assertAlmostEqual(
            about_link.location['y'] + about_link.size['height'] / 2,
            70,
            delta=50
        )
