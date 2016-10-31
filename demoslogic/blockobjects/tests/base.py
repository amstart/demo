from django.test import TestCase
from django.core.urlresolvers import reverse
from demoslogic.premises.models import Premise
from demoslogic.users.models import User

MODELNAME = 'premise'
MODEL = Premise
CREATEARGS = ['SubjectPredicate']

class BlockObjectsTests(TestCase):
    model = MODEL
    model_name = MODELNAME
    URL_login_redirect = reverse('account_login') + '?next='
    URL_detail = reverse(MODELNAME + 's:detail', args = [1])
    URL_create = reverse(MODELNAME + 's:create', args = CREATEARGS)

    def get_user(self, pk):
        return User.objects.get(pk = pk)

    def get_instance(self, **kwargs):
        user_id = kwargs.get('user_id', 1)
        if self.model == Premise:
            return self.model(user = self.get_user(user_id))
