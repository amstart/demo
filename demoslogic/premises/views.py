from dal import autocomplete
from switch import Switch

from django.views.generic import TemplateView, FormView
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q
from django.http import HttpResponseRedirect

from demoslogic.blockobjects import views

from . import forms, settings, models
# from .forms import PremiseCreateForm, PremiseVoteForm, SearchPremiseForm

class NewPremiseView(FormView):
    template_name = 'blockobjects/new.html'
    form_class = forms.NewPremiseForm
    success_url = reverse_lazy('premises:create')

    def get_context_data(self, **kwargs):
        context = super(NewPremiseView, self).get_context_data(**kwargs)
        context['model_name_lower'] = models.Premise.name_lower
        return context

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

class VerbSearchView(PremiseSearchView):
    template_name = 'premises/search.html'
    form_class = forms.SearchVerbForm
    suffix = 'verbs'

class AdjectiveSearchView(PremiseSearchView):
    template_name = 'premises/search.html'
    form_class = forms.SearchAdjectiveForm
    suffix = 'adjective'

class PremiseAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # if not self.request.user.is_authenticated():
        #     return Premise.objects.none()
        qs = models.Premise.objects.all()
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
        qs = models.Noun.objects.all()
        key_subject = self.forwarded.get('key_subject', None)
        key_object = self.forwarded.get('key_object', None)
        key_indirect_object = self.forwarded.get('key_indirect_object', None)
        if key_subject:
            qs = qs.exclude(id = key_subject)
        if key_object:
            qs = qs.exclude(id = key_object)
        if key_indirect_object:
            qs = qs.exclude(id = key_indirect_object)
        if self.q:
            qs = qs.filter(name__contains = self.q)
        return qs

class VerbAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = models.Verb.objects.all()
        if self.q:
            qs = qs.filter(name__contains = self.q)
        return qs

class AdjectiveAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = models.Adjective.objects.all()
        if self.q:
            qs = qs.filter(name__contains = self.q)
        return qs

class PremiseDetailView(views.DetailWithVoteView):
    model = models.Premise
    voteform = forms.PremiseVoteForm

    def get_context_data(self, **kwargs):
        context = super(PremiseDetailView, self).get_context_data(**kwargs)
        context['as_premise_set'] = self.object.premise1.filter()
        context['as_conclusion_set'] = self.object.conclusion.filter()
        return context

class PremiseUpdateView(views.UpdateVoteView):
    model = models.Premise
    voteform = forms.PremiseVoteForm

class PremiseCreateView(views.CreateObjectView):
    template_name = 'blockobjects/create_object.html'
    success_url = '/'
    model = models.Premise

    def get_form_class(self):
        premise_type = self.request.GET.get('premise_type')
        if premise_type:
            with Switch(int(premise_type)) as case:
                if case(settings.TYPE_CATEGORIZATION):
                    return forms.CategorizationCreateForm
                if case(settings.TYPE_COLLECTION):
                    return forms.CollectionCreateForm
                if case(settings.TYPE_COMPARISON):
                    return forms.ComparisonCreateForm
                if case(settings.TYPE_DEDUCTION):
                    return forms.DeductionCreateForm
                if case(settings.TYPE_DIAGNOSIS):
                    return forms.DiagnosisCreateForm
                if case(settings.TYPE_PROPOSAL):
                    return forms.ProposalCreateForm
        return forms.CategorizationCreateForm


class PremisesListView(views.ObjectListView):
    model = models.Premise

class DeletePremiseView(views.DeleteObjectView):
    model = models.Premise
    success_url = reverse_lazy('premises:index')
