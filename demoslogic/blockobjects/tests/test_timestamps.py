import datetime

from django.utils import timezone

from .base import BlockObjectsTests

class ObjectTimeStampMethodsTests(BlockObjectsTests):
    def test_old_object_was_not_published_recently(self):
        time = timezone.now() - datetime.timedelta(days = 30)
        old_object  =  self.create_object()
        setattr(old_object, 'pub_date', time)
        old_object.save()
        old_object = self.get_object(pk = old_object.pk)
        self.assertIs(old_object.was_published_recently(), False)

    def test_new_object_was_not_published_recently(self):
        time = timezone.now() - datetime.timedelta(hours = 1)
        recent_object = self.create_object()
        setattr(recent_object, 'pub_date', time)
        recent_object.save()
        recent_object = self.get_object(pk = recent_object.pk)
        self.assertIs(recent_object.was_published_recently(), True)
