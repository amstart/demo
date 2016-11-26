from django.test import TestCase
from django.core.urlresolvers import reverse
from demoslogic.premises.models import Premise, PremiseVote, Noun
from demoslogic.arguments.models import Argument, ArgumentVote
from demoslogic.users.models import User

MODEL = Premise
is_premise = MODEL == Premise
if is_premise:
    VOTEMODEL = PremiseVote
    CREATEPARAMS = [{'key_subject_id': 2, 'key_object_id': 1}]
    NOCREATEPARAMS = [{'key_subject_id': 1, 'key_object_id': 1}]
else:
    VOTEMODEL = ArgumentVote
    CREATEPARAMS = [{'aim': 1, 'premise1_if': 1, 'premise2_if': 1,
                     'premise1_id': 3, 'premise2_id': 2, 'conclusion_id': 1}]
    #no premise 2x and no argument 2x (testset has it already)
    NOCREATEPARAMS = [{'aim': 1, 'premise1_if': 1, 'premise2_if': 1,
                       'premise1_id': 3, 'premise2_id': 3, 'conclusion_id': 2},
                      {'aim': 1, 'premise1_if': 1, 'premise2_if': 1,
                       'premise1_id': 1, 'premise2_id': 2, 'conclusion_id': 3}]

POSTPARAMS = []
for parameter_set in CREATEPARAMS:
    new_parameter_set = {}
    for key, value in parameter_set.items():
        new_parameter_set[key.replace("_id", "")] = value
    POSTPARAMS.append(new_parameter_set)

NOPOSTPARAMS = []
for parameter_set in NOCREATEPARAMS:
    new_parameter_set = {}
    for key, value in parameter_set.items():
        new_parameter_set[key.replace("_id", "")] = value
    NOPOSTPARAMS.append(new_parameter_set)

class BlockObjectsTests(TestCase):
    fixtures = ['fixtures\\testusers.yaml', 'fixtures\\testset.yaml']
    model = MODEL
    vote_model = VOTEMODEL
    create_params = CREATEPARAMS
    post_params = POSTPARAMS
    no_create_params = NOCREATEPARAMS
    no_post_params = NOCREATEPARAMS
    is_premise = is_premise

    def URL_login_redirect(self):
        return reverse('account_login') + '?next='
    def URL_index(self):
        return reverse(MODEL.namespace + ':index')
    def URL_create(self):
        return reverse(MODEL.namespace + ':create')
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
