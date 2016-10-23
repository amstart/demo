from django.test import TestCase
from django.core.urlresolvers import reverse

from ..models import Premise


class URLTest(TestCase):
    fixtures = ['fixtures\\testset.yaml']

    def test_premises_url_resolves_to_index_page_view(self):
        response = self.client.get(reverse('premises:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'premises/index.html')

    def test_premises_with_number_resolves_to_detail_page_with_extra_radio_button_hidden(self):
        response = self.client.get(reverse('premises:detail', args = [1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'premises/detail.html')
        self.assertNotContains(response, '---')

# class AnonymousTest(TestCase):
#     fixtures = ['fixtures\\testset.yaml']
#
#     def test_delete_button_not_there_for_anonymous(self):
#         detail_url = reverse('premises:detail', args = [str(1)])
#         response_anonymous = self.client.get(detail_url)
#         self.assertNotContains(response_anonymous, "id='id_delete'")
