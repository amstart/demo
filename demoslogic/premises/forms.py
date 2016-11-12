from dal import autocomplete
from django import forms

from demoslogic.blockobjects.forms import VoteForm, SearchForm

from .models import Premise, Noun, Predicate, CategorizationVote

class SearchPremiseForm(SearchForm):
    search_id = forms.ModelChoiceField(label = "", queryset=Premise.objects.all(),
                                            widget=autocomplete.ModelSelect2(
                                            url = 'premises:autocomplete',
                                            attrs = {'data-minimum-input-length': 0}))

class SearchNounForm(SearchForm):
    search_id = forms.ModelChoiceField(label = "", queryset=Premise.objects.all(),
                                            widget=autocomplete.ModelSelect2(
                                            url = 'premises:nouns_autocomplete',
                                            attrs = {'data-minimum-input-length': 0}))
class SearchPredicateForm(SearchForm):
    search_id = forms.ModelChoiceField(label = "", queryset=Premise.objects.all(),
                                            widget=autocomplete.ModelSelect2(
                                            url = 'premises:predicates_autocomplete',
                                            attrs = {'data-minimum-input-length': 0}))

class CategorizationVoteForm(VoteForm):
    class Meta:
        model = CategorizationVote
        fields = ['value']
        widgets = {'value': forms.RadioSelect}
        labels = {'value': "How accurate do you think this categorization is?"}
        # empty_labels = {'value': None}


class PremiseCreateForm(forms.ModelForm):
    class Meta:
        model = Premise
        fields = ['premise_type', 'key_subject', 'key_predicate']
        widgets = {
            'key_subject': autocomplete.ModelSelect2(url = 'premises:nouns_autocomplete_create'),
            'key_predicate': autocomplete.ModelSelect2(url = 'premises:predicates_autocomplete_create'),
        }
