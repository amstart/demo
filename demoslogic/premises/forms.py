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

class AbstractForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AbstractForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = True
    class Meta:
        abstract = True

class WithComplementedObjectInputForm(AbstractForm):
    class Meta:
        model = Premise
        fields = ['subject', 'predicate', 'object', 'complement']

class WithObjectInputForm(AbstractForm):
    class Meta:
        model = Premise
        fields = ['subject', 'predicate', 'object']

class WithComplementInputForm(AbstractForm):
    class Meta:
        model = Premise
        fields = ['subject', 'predicate', 'complement']

class SubjectPredicateInputForm(AbstractForm):
        class Meta:
            model = Premise
            fields = ['subject', 'predicate']
