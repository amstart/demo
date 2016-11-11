from .base import FunctionalTest
from demoslogic.premises.models import Premise
from demoslogic.arguments.models import Argument

class NetworkGraphTest(FunctionalTest):
    fixtures = ['fixtures\\testset.yaml']

    def test_right_number_of_elements(self):
        argument_count = Argument.objects.count()
        premise_count = Premise.objects.count()
        self.create_pre_authenticated_session("Alfons")
        self.browser.find_element_by_link_text('Network').click()
        self.browser.implicitly_wait(2)
        self.browser.find_element_by_tag_name('circle')
        page_text = self.browser.find_element_by_tag_name('body').get_attribute('innerHTML').encode('unicode_escape')
        self.assertEqual(page_text.count(b'<circle'), argument_count + premise_count)
        self.assertEqual(page_text.count(b'class="forcelink'), argument_count * 3)
