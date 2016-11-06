from switch import Switch
from dal import autocomplete

from django.db.models import Q
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse, reverse_lazy

from demoslogic.blockobjects import views
from demoslogic.premises.models import Premise

from .models import Argument
from .forms import ArgumentInputForm, ArgumentVoteForm



class PremiseAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # if not self.request.user.is_authenticated():
        #     return Premise.objects.none()
        qs = Premise.objects.all()
        if self.q:
            # qs = Premise.objects.raw("SELECT * FROM Premise WHERE %s == CONCAT(premise1, premise2)", [self.q])
            qs = qs.filter(Q(subject__contains=self.q)
                           | Q(predicate__contains=self.q)
                           | Q(object__contains=self.q)
                           | Q(complement__contains=self.q))
        return qs

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

    def get_queryset(self):
        return Argument.objects.all().select_related('conclusion')

class DeleteArgumentView(views.DeleteObjectView):
    model = Argument
    success_url = reverse_lazy('arguments:index')
