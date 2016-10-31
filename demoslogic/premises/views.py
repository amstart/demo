from switch import Switch

from django.views.generic import TemplateView, DeleteView
from django.core.urlresolvers import reverse, reverse_lazy

from demoslogic.blockobjects.views import DetailWithVoteView, UpdateVoteView, CreateObjectView, ObjectListView

from .models import Premise
from .forms import SubjectPredicateInputForm, WithComplementedObjectInputForm, WithObjectInputForm, WithComplementInputForm
from .forms import CategorizationVoteForm

class PremiseDetailView(DetailWithVoteView):
    model = Premise
    voteform = CategorizationVoteForm()

class PremiseUpdateView(UpdateVoteView):
    model = Premise
    voteform = CategorizationVoteForm()

class NewPremiseView(TemplateView):
    template_name = 'premises/new_premise.html'

class PremiseCreateView(CreateObjectView):
    template_name = 'blockobjects/create_object.html'
    success_url = '/'
    model = Premise

    def get_context_data(self, **kwargs):
        context = super(PremiseCreateView, self).get_context_data(**kwargs)
        context['object_name_upper'] = self.model.__name__
        context['object_name_lower'] = self.model.__name__.lower()
        return context

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

class PremisesListView(ObjectListView):
    model = Premise

class DeletePremiseView(DeleteView):
    template_name = 'blockobjects/delete_object.html'
    model = Premise
    success_url = reverse_lazy('premises:index')
