from dal import autocomplete
from switch import Switch

from django.views.generic import TemplateView, FormView
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q
from django.http import HttpResponseRedirect

from demoslogic.blockobjects import views

from .models import Premise, Predicate, Noun, Complement
from . import forms
# from .forms import PremiseCreateForm, CategorizationVoteForm, SearchPremiseForm

class PremiseSearchView(FormView):
    template_name = 'premises/search.html'
    form_class = forms.SearchPremiseForm
    success_url = '/'
    suffix = 'detail'

    def get(self, request, *args, **kwargs):
        search_id = request.GET.get('search_id')
        if search_id:
            return HttpResponseRedirect(reverse('premises:' + self.suffix, args = [search_id]))
        else:
            return super(PremiseSearchView, self).get(request, *args, **kwargs)

class NounSearchView(PremiseSearchView):
    template_name = 'premises/search.html'
    form_class = forms.SearchNounForm
    suffix = 'nouns'

class PredicateSearchView(PremiseSearchView):
    template_name = 'premises/search.html'
    form_class = forms.SearchPredicateForm
    suffix = 'predicates'

class ComplementSearchView(PremiseSearchView):
    template_name = 'premises/search.html'
    form_class = forms.SearchComplementForm
    suffix = 'complements'

class PremiseAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # if not self.request.user.is_authenticated():
        #     return Premise.objects.none()
        qs = Premise.objects.all()
        premise1 = self.forwarded.get('premise1', None)
        premise2 = self.forwarded.get('premise2', None)
        conclusion = self.forwarded.get('conclusion', None)
        if premise1:
            qs = qs.exclude(id = premise1)
        if premise2:
            qs = qs.exclude(id = premise2)
        if conclusion:
            qs = qs.exclude(id = conclusion)
        if self.q:
            qs = qs.filter(sentence__contains = self.q)
        return qs

class NounAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Noun.objects.all()
        if self.q:
            qs = qs.filter(name__contains = self.q)
        return qs

class PredicateAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Predicate.objects.all()
        if self.q:
            qs = qs.filter(name__contains = self.q)
        return qs

class ComplementAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Complement.objects.all()
        if self.q:
            qs = qs.filter(name__contains = self.q)
        return qs

class PremiseDetailView(views.DetailWithVoteView):
    model = Premise
    voteform = forms.CategorizationVoteForm()

    def get_context_data(self, **kwargs):
        context = super(PremiseDetailView, self).get_context_data(**kwargs)
        context['as_premise_set'] = self.object.premise1.filter()
        context['as_conclusion_set'] = self.object.conclusion.filter()
        return context

class PremiseUpdateView(views.UpdateVoteView):
    model = Premise
    voteform = forms.CategorizationVoteForm()

class PremiseCreateView(views.CreateObjectView):
    template_name = 'blockobjects/create_object.html'
    success_url = '/'
    model = Premise
    def get_form_class(self):
        return forms.PremiseCreateForm

class PremisesListView(views.ObjectListView):
    model = Premise

class DeletePremiseView(views.DeleteObjectView):
    model = Premise
    success_url = reverse_lazy('premises:index')
