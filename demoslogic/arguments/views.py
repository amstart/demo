from switch import Switch

from django.views.generic import TemplateView
from django.core.urlresolvers import reverse, reverse_lazy

from demoslogic.blockobjects import views

from .models import Argument
from .forms import ArgumentInputForm, ArgumentVoteForm

class ArgumentDetailView(views.DetailWithVoteView):
    model = Argument
    voteform = ArgumentVoteForm()

class ArgumentUpdateView(views.UpdateVoteView):
    model = Argument
    voteform = ArgumentVoteForm()

class NewArgumentView(TemplateView):
    template_name = 'arguments/new_argument.html'

class ArgumentCreateView(views.CreateObjectView):
    template_name = 'blockobjects/create_object.html'
    success_url = '/'
    model = Argument

    def get_form_class(self):
        return ArgumentInputForm

class ArgumentsListView(views.ObjectListView):
    model = Argument

class DeleteArgumentView(views.DeleteObjectView):
    model = Argument
    success_url = reverse_lazy('arguments:index')
