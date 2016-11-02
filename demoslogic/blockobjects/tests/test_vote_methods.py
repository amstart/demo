from demoslogic.users.models import User

from .base import BlockObjectsTests

class VoteMethodTests(BlockObjectsTests):
    def test_updates_to_correct_vote_value(self):
        new_vote = self.create_vote_object(value = 2)
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
