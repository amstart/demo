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
from .views import IndexView


homepage_url = 'http://localhost:8000'


class TemplateTest(TestCase):


    def test_premises_url_resolves_to_index_page_view(self):
        #self.client.login(username='Jochen', password='b83cfg')  # defined in fixture or with factory in setUp()
        response = self.client.get(reverse('premises:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/index.html')


class ViewTest(TestCase):


    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='Alfons', email='al@fons.com', password='top-secretary')

    def test_home_page_can_save_a_new_premise(self):
        post_data = {'item_text': 'A new premise'}
        request = self.factory.post('fake/path', post_data)
        view = IndexView.as_view()
        view(request)
        premises = Premise.objects.all()
        self.assertEqual('A new premise', premises[0].text)

    def test_new_premise_shows_up_in_index(self):
        new_premise = Premise(text='A new premise', pub_date=timezone.now())
        new_premise.save()
        response = self.client.get(reverse('premises:index'))
        self.assertIn('A new premise', response.content.decode())


class PremiseMethodTests(TestCase):


    def test_was_published_recently_with_future_premise(self):
        """
        was_published_recently() should return False for premises whose
        pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_premise = Premise(pub_date=time)
        self.assertIs(future_premise.was_published_recently(), False)

    def test_was_published_recently_with_old_premise(self):
        """
        was_published_recently() should return False for premises whose
        pub_date is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=30)
        old_premise = Premise(pub_date=time)
        self.assertIs(old_premise.was_published_recently(), False)

    def test_was_published_recently_with_recent_premise(self):
        """
        was_published_recently() should return True for premises whose
        pub_date is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_premise = Premise(pub_date=time)
        self.assertIs(recent_premise.was_published_recently(), True)
