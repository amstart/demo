from django.test import TestCase
from django.core.urlresolvers import reverse

from demoslogic.users.models import User
from ..models import Premise


class CanDeletePremiseTest(TestCase):
    fixtures = ['fixtures\\testset.yaml']

    def setUp(self):
        self.new_premise = Premise.objects.create(user_id = 1)
        self.detail_url = reverse('premises:detail', args = [self.new_premise.pk])
        self.delete_url = reverse('premises:delete', args = [self.new_premise.pk])

    def assertCanDelete(self):
        response = self.client.get(self.detail_url)
        self.assertContains(response, "id='id_delete'")
        response = self.client.get(self.delete_url)
        print(self.delete_url)
        self.assertContains(response, "<form")

    def assertCannotDelete(self):
        response = self.client.get(self.detail_url)
        self.assertNotContains(response, "id='id_delete'")
        response = self.client.get(self.delete_url)
        self.assertNotContains(response, "<form")

    def test_delete_button_shows_up(self):
        self.logged_in = self.client.force_login(user = User.objects.get(pk = 1))
        self.assertCanDelete()

    def test_delete_button_not_there_for_old_premise(self):
        self.logged_in = self.client.force_login(user = User.objects.get(pk = 1))
        self.detail_url = reverse('premises:detail', args = [1])
        self.delete_url = reverse('premises:delete', args = [1])
        self.assertCannotDelete()

    def test_delete_button_not_there_for_other_user(self):
        self.logged_in = self.client.force_login(user = User.objects.get(pk = 2))
        self.assertCannotDelete()

    def test_delete_button_not_there_for_anonymous(self):
        self.assertCannotDelete()

class CanVotePremiseTest(TestCase):
    fixtures = ['fixtures\\testset.yaml']

    def setUp(self):
        self.detail_url = reverse('premises:detail', args = [1])

    def test_right_number_of_radiobuttons(self):
        response = self.client.get(self.detail_url)
        self.assertContains(response, "class=\"radio\"", count = 4)
