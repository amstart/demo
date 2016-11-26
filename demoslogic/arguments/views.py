from switch import Switch

from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, FormView
from django.core.urlresolvers import reverse, reverse_lazy

from demoslogic.blockobjects import views
from demoslogic.premises.models import Premise
from .models import Argument
from . import forms

class NewArgumentView(FormView):
    template_name = 'blockobjects/new.html'
    form_class = forms.NewArgumentForm
    success_url = reverse_lazy('arguments:create')

    def get_context_data(self, **kwargs):
        context = super(NewArgumentView, self).get_context_data(**kwargs)
        context['model_name_lower'] = Argument.name_lower
        return context


class ArgumentDetailView(views.DetailWithVoteView):
    model = Argument
    voteform = forms.ArgumentVoteForm

class ArgumentUpdateView(views.UpdateVoteView):
    model = Argument
    voteform = forms.ArgumentVoteForm

class ArgumentCreateView(views.CreateObjectView):
    template_name = 'blockobjects/create_object.html'
    success_url = '/'
    model = Argument

    def get_form_class(self):
        return forms.ArgumentCreateForm

class ArgumentsListView(views.ObjectListView):
    model = Argument

    def get_queryset(self):
        return Argument.objects.all().select_related('conclusion')

class DeleteArgumentView(views.DeleteObjectView):
    model = Argument
    success_url = reverse_lazy('arguments:index')
