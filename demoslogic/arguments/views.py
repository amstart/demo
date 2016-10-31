from switch import Switch

from django.views.generic import TemplateView, DeleteView
from django.core.urlresolvers import reverse, reverse_lazy

from demoslogic.blockobjects.views import DetailWithVoteView, UpdateVoteView, CreateObjectView, ObjectListView

from .models import Argument
from .forms import SubjectPredicateInputForm, WithComplementedObjectInputForm, WithObjectInputForm, WithComplementInputForm
from .forms import CategorizationVoteForm

class ArgumentDetailView(DetailWithVoteView):
    model = Argument
    voteform = CategorizationVoteForm()

class ArgumentUpdateView(UpdateVoteView):
    model = Argument
    voteform = CategorizationVoteForm()

class NewArgumentView(TemplateView):
    template_name = 'premises/new_premise.html'

class ArgumentCreateView(CreateObjectView):
    template_name = 'premises/create_premise.html'
    success_url = '/'
    model = Argument

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

class ArgumentsListView(ObjectListView):
    model = Argument

class DeleteArgumentView(DeleteView):
    template_name = 'blockobjects/delete_object.html'
    model = Argument
    success_url = reverse_lazy('premises:index')
