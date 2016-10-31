import datetime

from django.utils import timezone

from .base import BlockObjectsTests


class ObjectTimeStampMethodsTests(BlockObjectsTests):
    fixtures = ['fixtures\\testset.yaml']

    def test_old_object_was_not_published_recently(self):
        time = timezone.now() - datetime.timedelta(days = 30)
        old_object  =  self.create_object()
        setattr(old_object, 'pub_date', time)
        self.assertIs(old_object.was_published_recently(), False)

    def test_new_object_was_not_published_recently(self):
        time = timezone.now() - datetime.timedelta(hours = 1)
        recent_object = self.create_object()
        setattr(recent_object, 'pub_date', time)
        self.assertIs(recent_object.was_published_recently(), True)
