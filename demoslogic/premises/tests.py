from django.test import TestCase
from django.core.urlresolvers import reverse

class URLTest(TestCase):
    fixtures = ['fixtures\\testset.yaml']

    def test_new_premise_view(self):
        response = self.client.get(reverse('premises:new'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'premises/new_premise.html')
# class AnonymousTest(TestCase):
#     fixtures = ['fixtures\\testset.yaml']
#
#     def test_delete_button_not_there_for_anonymous(self):
#         detail_url = reverse('premises:detail', args = [str(1)])
#         response_anonymous = self.client.get(detail_url)
#         self.assertNotContains(response_anonymous, "id='id_delete'")
