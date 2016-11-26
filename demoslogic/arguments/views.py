from switch import Switch

from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, View
from django.core.urlresolvers import reverse, reverse_lazy

from demoslogic.blockobjects import views
from demoslogic.premises.models import Premise

from .models import Argument
from .forms import ArgumentInputForm, ArgumentVoteForm

class NewArgumentView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('arguments:create'))

class ArgumentDetailView(views.DetailWithVoteView):
    model = Argument
    voteform = ArgumentVoteForm

class ArgumentUpdateView(views.UpdateVoteView):
    model = Argument
    voteform = ArgumentVoteForm

class ArgumentCreateView(views.CreateObjectView):
    template_name = 'blockobjects/create_object.html'
    success_url = '/'
    model = Argument

    def get_form_class(self):
        return ArgumentInputForm

class ArgumentsListView(views.ObjectListView):
    model = Argument

    def get_queryset(self):
        return Argument.objects.all().select_related('conclusion')

class DeleteArgumentView(views.DeleteObjectView):
    model = Argument
    success_url = reverse_lazy('arguments:index')
