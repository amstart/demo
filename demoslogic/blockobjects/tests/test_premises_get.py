from django.core.urlresolvers import reverse

from demoslogic.users.models import User

from .base import BlockObjectsTests

class CanDeleteObjectTest(BlockObjectsTests):
    fixtures = ['fixtures\\testset.yaml']

    def setUp(self):
        new_premise = self.create_object()
        self.detail_url = reverse(self.model.name + 's:detail', args = [new_premise.pk])
        self.delete_url = reverse(self.model.name + 's:delete', args = [new_premise.pk])

    def assertCanDelete(self):
        response = self.client.get(self.detail_url)
        self.assertContains(response, "id='id_delete'")
        response = self.client.get(self.delete_url)
        self.assertContains(response, "<form")

    def assertCannotDelete(self):
        response = self.client.get(self.detail_url)
        self.assertNotContains(response, "id='id_delete'")
        response = self.client.get(self.delete_url)
        self.assertNotContains(response, "<form")

    def test_delete_button_shows_up(self):
        self.login()
        self.assertCanDelete()

    def test_delete_button_not_there_for_old_premise(self):
        self.login()
        self.detail_url = self.URL_detail
        self.delete_url = self.URL_delete
        self.assertCannotDelete()

    def test_delete_button_not_there_for_other_user(self):
        self.login(user_id = 2)
        self.assertCannotDelete()

    def test_delete_button_not_there_for_anonymous(self):
        self.assertCannotDelete()

class CanVoteObjectTest(BlockObjectsTests):
    fixtures = ['fixtures\\testset.yaml']

    def setUp(self):
        super(CanVoteObjectTest, self).setUp()
        self.detail_url = reverse('premises:detail', args = [1])

    def test_right_number_of_radiobuttons_for_anonymous(self):
        response = self.client.get(self.detail_url)
        choices = self.vote_model._meta.get_field('value').choices
        self.assertContains(response, "class=\"radio\"", count = len(choices))

    def test_right_number_of_radiobuttons_for_user(self):
        self.client.force_login(user = User.objects.get(pk = 1))
        response = self.client.get(self.detail_url)
        choices = self.vote_model._meta.get_field('value').choices
        self.assertContains(response, "class=\"radio\"", count = len(choices))

class SeeVoteObjectTest(BlockObjectsTests):
    fixtures = ['fixtures\\testset.yaml']

    def setUp(self):
        super(SeeVoteObjectTest, self).setUp()
        self.detail_url = reverse('premises:detail', args = [3])

    def test_see_options(self):
        self.client.force_login(user = User.objects.get(pk = 1))
        choices = self.vote_model._meta.get_field('value').choices
        response = self.client.get(self.detail_url)
        bar_labels = [x[1] for x in choices]
        for label in bar_labels:
            self.assertContains(response, label + ":", count = 1)

    def test_see_vote(self):
        self.client.force_login(user = User.objects.get(pk = 1))
        response = self.client.get(self.detail_url)
        self.assertContains(response, "1 (you)", count = 1)
