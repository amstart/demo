from django.test import TestCase
from django.core.urlresolvers import reverse

class RedirectsIfAnonymous(TestCase):
    fixtures = ['fixtures\\testset.yaml']

    def test_redirects_for_vote(self):
        redirect = self.client.post(reverse('premises:detail', args = [1]))
        self.assertRedirects(redirect, reverse('account_login') + '?next=' + reverse('premises:detail', args = [1]))

    def test_redirects_for_premise_creation(self):
        redirect = self.client.post(reverse('premises:create', args = ['SubjectPredicate']))
        self.assertRedirects(redirect, reverse('account_login') + '?next=' + reverse('premises:create', args = ['SubjectPredicate']))
