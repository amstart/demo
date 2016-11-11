from django.test import TestCase
from django.core.urlresolvers import reverse
from demoslogic.premises.models import Premise, CategorizationVote
from demoslogic.arguments.models import Argument, ArgumentVote
from demoslogic.users.models import User

MODEL = Argument
is_premise = MODEL == Premise
if is_premise:
    CREATEARG = ['WithComplementedObject']
    VOTEMODEL = CategorizationVote
    CREATEPARAMS = [{'subject': 'peas', 'predicate': 'make', 'object': 'peacocks', 'complement': 'cry'}]
    POSTPARAMS = [{'subject': 'peas', 'predicate': 'make', 'object': 'peacocks', 'complement': 'cry'}]
    NOPOSTPARAMS = [{'subject': '', 'predicate': 'make', 'object': 'peacocks', 'complement': 'cry'}]
else:
    CREATEARG = []
    VOTEMODEL = ArgumentVote
    CREATEPARAMS = [{'aim': 1, 'premise1_id': 1, 'premise2_id': 2, 'conclusion_id': 3}]
    POSTPARAMS = [{'aim': 1, 'premise1': 1, 'premise2': 2, 'conclusion': 3}]
    NOPOSTPARAMS = [{'aim': 1, 'premise1': 1, 'premise2': 1, 'conclusion': 2}]

class BlockObjectsTests(TestCase):
    fixtures = ['fixtures\\testset.yaml']
    model = MODEL
    vote_model = VOTEMODEL
    create_params = CREATEPARAMS
    post_params = POSTPARAMS
    no_post_params = NOPOSTPARAMS
    is_premise = is_premise

    def URL_login_redirect(self):
        return reverse('account_login') + '?next='
    def URL_index(self):
        return reverse(MODEL.namespace + ':index')
    def URL_create(self, args = CREATEARG):
        return reverse(MODEL.namespace + ':create', args = args)
    def URL_detail(self, pk = 1):
        return reverse(MODEL.namespace + ':detail', args = [pk])
    def URL_delete(self, pk = 1):
        return reverse(MODEL.namespace + ':delete', args = [pk])

    def get_user(self, pk):
        return User.objects.get(pk = pk)

    def get_object(self, pk):
        return self.model.objects.get(pk = pk)

    def create_object(self, **kwargs):
        user_id = kwargs.get('user_id', 1)
        return self.model.objects.create(user = self.get_user(user_id), **self.create_params[0])

    def create_vote_object(self, **kwargs):
        user_id = kwargs.get('user_id', 1)
        object_id = kwargs.get('object_id', 1)
        value = kwargs.get('value', 1)
        return self.vote_model.objects.create(user = self.get_user(user_id),
                               object = self.get_object(object_id),
                               value = value)

    def login(self, **kwargs):
        user_id = kwargs.get('user_id', 1)
        return self.client.force_login(user = self.get_user(user_id))
