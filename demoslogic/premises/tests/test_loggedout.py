from django.test import TestCase
from django.core.urlresolvers import reverse

from ..models import Premise


class TemplateTest(TestCase):

    def test_premises_url_resolves_to_index_page_view(self):
        response = self.client.get(reverse('premises:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'premises/index.html')
