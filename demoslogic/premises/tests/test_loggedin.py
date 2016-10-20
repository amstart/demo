import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse

from demoslogic.users.models import User
from ..models import Premise

premise_core = {'subject':'peas', 'predicate':'make', 'object':'peacocks', 'complement':'cry'}


class ViewPremiseTest(TestCase):
    def setUp(self):
        # self.factory = RequestFactory()
        self.user = User.objects.create_user(username = 'Alfons')
        self.logged_in = self.client.force_login(user = self.user)
        self.new_premise = Premise.objects.create(user = self.user)
        self.detail_url = reverse('premises:detail', args = [str(self.new_premise.pk)])

    def test_vote_form_shows_up(self):
        response = self.client.get(self.detail_url)
        self.assertContains(response_user, "id='id_delete'")

    def test_delete_button_only_there_for_correct_user(self):
        time = timezone.now() - datetime.timedelta(days = 30)
        staged_premise  =  Premise.objects.create(user = self.user)
        setattr(staged_premise, 'pub_date', time)
        staged_premise.save()
        response_user = self.client.get(self.detail_url)
        response_user_staged_premise = self.client.get(reverse('premises:detail', args = [str(staged_premise.pk)]))
        self.assertNotContains(response_user_staged_premise, "id='id_delete'")
        self.assertContains(response_user, "id='id_delete'")
        self.client.logout()
        response_anonymous = self.client.get(detail_url)
        self.assertNotContains(response_anonymous, "id='id_delete'")
        self.otheruser = User.objects.create_user(username = 'Fred')
        self.logged_in = self.client.force_login(user = self.otheruser)
        response_otheruser = self.client.get(detail_url)
        self.assertNotContains(response_otheruser, "id='id_delete'")


class CreatePremiseTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username = 'Alfons')
        self.logged_in = self.client.force_login(user = self.user)

    def test_premises_show_up_for_everyone_in_relevant_pages(self):
        self.responseFull = self.client.post(reverse('premises:create', args = ['WithComplementedObject']), premise_core)
        self.client.post(reverse('premises:create', args = ['WithObject']), premise_core)
        self.client.post(reverse('premises:create', args = ['WithComplement']), premise_core)
        self.client.post(reverse('premises:create', args = ['SubjectPredicate']), premise_core)
        premises = Premise.objects.all()
        detail_url = reverse('premises:detail', args = [str(premises[0].pk)])
        self.assertRedirects(self.responseFull, detail_url)
        response_index = self.client.get(reverse('premises:index'))
        response_unstaged = self.client.get(reverse('premises:unstaged'))
        response_detail = self.client.get(detail_url)
        expected_count = {'subject':4, 'predicate':4, 'object':2, 'complement':2}
        for key, value in premise_core.items():
            self.assertContains(response_index, value, count = expected_count[key])
            self.assertContains(response_unstaged, value, count = expected_count[key])
            self.assertContains(response_detail, value)
            self.assertContains(response_index, "class=\"" + key + "\"")
            self.assertContains(response_unstaged, "class=\"" + key + "\"")
            self.assertContains(response_detail, "class=\"" + key + "\"")
