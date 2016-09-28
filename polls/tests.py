import datetime

from django.utils import timezone
from django.test import TestCase

from .models import Premise


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
