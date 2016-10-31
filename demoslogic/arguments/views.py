from switch import Switch

from django.views.generic import TemplateView, DeleteView
from django.core.urlresolvers import reverse, reverse_lazy

from demoslogic.blockobjects.views import DetailWithVoteView, UpdateVoteView, CreateObjectView, ObjectListView

from .models import Argument
from .forms import ArgumentInputForm, ArgumentVoteForm

class ArgumentDetailView(DetailWithVoteView):
    model = Argument
    voteform = ArgumentVoteForm()

class ArgumentUpdateView(UpdateVoteView):
    model = Argument
    voteform = ArgumentVoteForm()

class NewArgumentView(TemplateView):
    template_name = 'arguments/new_argument.html'

class ArgumentCreateView(CreateObjectView):
    template_name = 'blockobjects/create_object.html'
    success_url = '/'
    model = Argument

    def get_context_data(self, **kwargs):
        context = super(ArgumentCreateView, self).get_context_data(**kwargs)
        context['object_name_upper'] = self.model.__name__
        context['object_name_lower'] = self.model.__name__.lower()
        return context

    def get_form_class(self):
        return ArgumentInputForm

class ArgumentsListView(ObjectListView):
    model = Argument

class DeleteArgumentView(DeleteView):
    template_name = 'blockobjects/delete_object.html'
    model = Argument
    success_url = reverse_lazy('arguments:index')
