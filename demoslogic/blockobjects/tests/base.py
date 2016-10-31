from django.test import TestCase
from django.core.urlresolvers import reverse
from demoslogic.premises.models import Premise, CategorizationVote
from demoslogic.arguments.models import Argument
from demoslogic.users.models import User

MODEL = Argument
VOTEMODEL = CategorizationVote
if MODEL == Premise:
    CREATEARGS = ['SubjectPredicate']
else:
    CREATEARGS = []


class BlockObjectsTests(TestCase):
    model = MODEL
    vote_model = VOTEMODEL
    URL_login_redirect = reverse('account_login') + '?next='
    URL_index = reverse(MODEL.name + 's:index')
    URL_detail = reverse(MODEL.name + 's:detail', args = [1])
    URL_create = reverse(MODEL.name + 's:create', args = CREATEARGS)
    URL_delete = reverse(MODEL.name + 's:delete', args = [1])

    def get_user(self, pk):
        return User.objects.get(pk = pk)

    def get_object(self, pk):
        return self.model.objects.get(pk = pk)

    def create_object(self, **kwargs):
        user_id = kwargs.get('user_id', 1)
        if self.model == Premise:
            return self.model.objects.create(user = self.get_user(user_id))

    def create_vote_object(self, **kwargs):
        user_id = kwargs.get('user_id', 1)
        object_id = kwargs.get('object_id', 1)
        value = kwargs.get('value', 1)
        if self.vote_model == CategorizationVote:
            return self.vote_model.objects.create(user = self.get_user(user_id),
                                   object = self.get_object(object_id),
                                   value = value)

    def login(self, **kwargs):
        user_id = kwargs.get('user_id', 1)
        return self.client.force_login(user = self.get_user(user_id))
