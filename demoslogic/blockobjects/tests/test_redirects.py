from django.core.urlresolvers import reverse

from .base import BlockObjectsTests

class RedirectsIfAnonymous(BlockObjectsTests):
    def test_redirects_for_vote(self):
        redirect = self.client.post(self.URL_detail())
        self.assertRedirects(redirect, self.URL_login_redirect() + self.URL_detail())

    def test_redirects_for_premise_creation(self):
        redirect = self.client.post(self.URL_create())
        self.assertRedirects(redirect, self.URL_login_redirect() + self.URL_create())
