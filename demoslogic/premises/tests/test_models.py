from django.test import TestCase

from demoslogic.users.models import User
from ..models import Premise, CategorizationVote

class VoteMethodTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username = 'Alfons')
        self.premise = Premise.objects.create(user=self.user)

    def test_updates_to_correct_vote_value(self):
        new_vote = CategorizationVote.objects.create(user = self.user, object = self.premise, value = 2)
        last_voted = new_vote.last_voted
        new_vote.update(10)
        self.assertEqual(new_vote.value, 2)
        self.assertEqual(new_vote.last_voted, last_voted)
        new_vote.update(1)
        self.assertEqual(new_vote.value, 1)
        self.assertNotEqual(new_vote.last_voted, last_voted)



        # post_data = {'item_text': 'peas'}
        # request = self.factory.post('premises/new', post_data)
        # view = IndexView.as_view()
        # view(request)
