from django.test import TestCase
from django.core.urlresolvers import reverse

from demoslogic.users.models import User
from ..models import Premise

premise_core = {'subject':'peas', 'predicate':'make', 'object':'peacocks', 'complement':'cry'}

class CreatePremiseTest(TestCase):
    fixtures = ['fixtures\\testusers.yaml']

    def setUp(self):
        self.logged_in = self.client.force_login(user = User.objects.get(pk = 1))

    def test_redirecting_works(self):
        self.response = self.client.post(reverse('premises:create', args = ['WithComplementedObject']), premise_core)
        premises = Premise.objects.all()
        detail_url = reverse('premises:detail', args = [premises[0].pk])
        self.assertRedirects(self.response, detail_url)

    def test_premises_show_up_for_everyone_in_relevant_pages(self):
        self.client.post(reverse('premises:create', args = ['WithComplementedObject']), premise_core)
        self.client.post(reverse('premises:create', args = ['WithObject']), premise_core)
        self.client.post(reverse('premises:create', args = ['WithComplement']), premise_core)
        self.client.post(reverse('premises:create', args = ['SubjectPredicate']), premise_core)
        premises = Premise.objects.all()
        detail_url = reverse('premises:detail', args = [str(premises[0].pk)])
        response_index = self.client.get(reverse('premises:index'))
        response_unstaged = self.client.get(reverse('premises:unstaged'))
        response_detail = self.client.get(detail_url)
        expected_count = {'subject':4, 'predicate':4, 'object':2, 'complement':2}
        self.client.logout()
        for key, value in premise_core.items():
            self.assertContains(response_index, value, count = expected_count[key])
            self.assertContains(response_unstaged, value, count = expected_count[key])
            self.assertContains(response_detail, value)
            self.assertContains(response_index, "class=\"" + key + "\"")
            self.assertContains(response_unstaged, "class=\"" + key + "\"")
            self.assertContains(response_detail, "class=\"" + key + "\"")
