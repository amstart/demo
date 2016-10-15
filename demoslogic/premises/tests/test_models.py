import datetime

from django.utils import timezone
from django.test import TestCase

from demoslogic.users.models import User
from ..models import Premise, CategorizationVote

class VoteMethodTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username = 'Alfons')
        self.premise = Premise(user=self.user)

    def test_vote_is_saved(self):
        new_vote = CategorizationVote.objects.castvote(user = self.user, object = self.premise, vote_accuracy = 2)
        self.assertEqual(new_vote.getvote, 2)

class PremiseMethodTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username = 'Alfons')

    def test_was_published_recently_with_old_premise(self):
        """
        was_published_recently() should return False for premises whose
        pub_date is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days = 30)
        old_premise  =  Premise(user=self.user)
        setattr(old_premise, 'pub_date', time)
        self.assertIs(old_premise.was_published_recently(), False)

    def test_was_published_recently_with_recent_premise(self):
        """
        was_published_recently() should return True for premises whose
        pub_date is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours = 1)
        recent_premise = Premise(user=self.user)
        setattr(recent_premise, 'pub_date', time)
        self.assertIs(recent_premise.was_published_recently(), True)

        # post_data = {'item_text': 'peas'}
        # request = self.factory.post('premises/new', post_data)
        # view = IndexView.as_view()
        # view(request)
