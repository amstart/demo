from dal import autocomplete
from django import forms

from demoslogic.blockobjects.forms import VoteForm, SearchForm

from .models import Premise, CategorizationVote

class SearchPremiseForm(SearchForm):
    premise_search = forms.ModelChoiceField(label = "", queryset=Premise.objects.all(),
                                            widget=autocomplete.ModelSelect2(
                                            url = 'premises:autocomplete',
                                            attrs = {'data-minimum-input-length': 0}))

class CategorizationVoteForm(VoteForm):
    class Meta:
        model = CategorizationVote
        fields = ['value']
        widgets = {'value': forms.RadioSelect}
        labels = {'value': "How accurate do you think this categorization is?"}
        # empty_labels = {'value': None}


class PremiseCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PremiseCreateForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = True

    class Meta:
        model = Premise
        fields = ['subject', 'predicate']
