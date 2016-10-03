import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import resolve
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.test import RequestFactory

from demoslogic.users.models import User
from .models import Premise
from .views import vote


premise_core = {'subject':'peas', 'predicate':'make', 'object':'peacocks', 'complement':'cry'}


class TemplateTest(TestCase):

    def test_premises_url_resolves_to_index_page_view(self):
        #self.client.login(username = 'Jochen', password = 'b83cfg')  # defined in fixture or with factory in setUp()
        response = self.client.get(reverse('premises:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/index.html')


class NewPremiseTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username = 'Alfons', email = 'al@fons.com', password = 'top-secretary')
        self.logged_in = self.client.login(username=self.user.username, password='top-secretary')
        # Create the different premises by POST and one by hand
        self.responseFull = self.client.post(reverse('premises:new') + 'WithComplementedObject', premise_core)
        self.client.post(reverse('premises:new') + 'WithObject', premise_core)
        self.client.post(reverse('premises:new') + 'WithComplement', premise_core)
        new_premise = Premise(**premise_core)
        new_premise.save()

    def test_premises_show_up_for_everyone_in_relevant_pages(self):
        premises = Premise.objects.all()
        detail_url = reverse('premises:detail', args = [str(premises[0].pk)])
        self.assertRedirects(self.responseFull, detail_url)
        responseIndex = self.client.get(reverse('premises:index'))
        responseUnstaged = self.client.get(reverse('premises:unstaged'))
        responseDetail = self.client.get(detail_url)
        expected_count = {'subject':4, 'predicate':4, 'object':3, 'complement':3}
        for key, value in premise_core.items():
            self.assertContains(responseIndex, value, count = expected_count[key])
            self.assertContains(responseUnstaged, value, count = expected_count[key])
            self.assertContains(responseDetail, value)


class PremiseMethodTests(TestCase):

    def test_was_published_recently_with_old_premise(self):
        """
        was_published_recently() should return False for premises whose
        pub_date is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days = 30)
        old_premise  =  Premise()
        setattr(old_premise, 'pub_date', time)
        self.assertIs(old_premise.was_published_recently(), False)

    def test_was_published_recently_with_recent_premise(self):
        """
        was_published_recently() should return True for premises whose
        pub_date is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours = 1)
        recent_premise = Premise()
        setattr(recent_premise, 'pub_date', time)
        self.assertIs(recent_premise.was_published_recently(), True)

        # post_data = {'item_text': 'peas'}
        # request = self.factory.post('premises/new', post_data)
        # view = IndexView.as_view()
        # view(request)
