from switch import Switch

from django.views.generic import TemplateView
from django.core.urlresolvers import reverse, reverse_lazy

from demoslogic.blockobjects import views

from .models import Premise
from .forms import SubjectPredicateInputForm, WithComplementedObjectInputForm, WithObjectInputForm, WithComplementInputForm
from .forms import CategorizationVoteForm

class PremiseDetailView(views.DetailWithVoteView):
    model = Premise
    voteform = CategorizationVoteForm()

class PremiseUpdateView(views.UpdateVoteView):
    model = Premise
    voteform = CategorizationVoteForm()

class NewPremiseView(TemplateView):
    template_name = 'premises/new_premise.html'

class PremiseCreateView(views.CreateObjectView):
    template_name = 'blockobjects/create_object.html'
    success_url = '/'
    model = Premise

    def get_form_class(self):
        with Switch(self.kwargs['mode']) as case:
            if case('SubjectPredicate'):
                return SubjectPredicateInputForm
            if case('WithComplementedObject'):
                return WithComplementedObjectInputForm
            if case('WithObject'):
                return WithObjectInputForm
            if case('WithComplement'):
                return WithComplementInputForm

class PremisesListView(views.ObjectListView):
    model = Premise

class DeletePremiseView(views.DeleteObjectView):
    model = Premise
    success_url = reverse_lazy('premises:index')
