from dal import autocomplete
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, HTML
from django import forms

from demoslogic.blockobjects.forms import VoteForm, SearchForm

from .models import Premise, Noun, Verb, Adjective, CategorizationVote

class SearchPremiseForm(SearchForm):
    search_id = forms.ModelChoiceField(label = "Find Statement:", queryset=Premise.objects.all(),
                                            widget=autocomplete.ModelSelect2(
                                            url = 'premises:autocomplete',
                                            attrs = {'data-minimum-input-length': 0}))

class SearchNounForm(SearchForm):
    search_id = forms.ModelChoiceField(label = "Find Noun:", queryset=Noun.objects.all(),
                                            widget=autocomplete.ModelSelect2(
                                            url = 'premises:nouns_autocomplete',
                                            attrs = {'data-minimum-input-length': 0}))
class SearchVerbForm(SearchForm):
    search_id = forms.ModelChoiceField(label = "Find Verb:", queryset=Verb.objects.all(),
                                            widget=autocomplete.ModelSelect2(
                                            url = 'premises:verbs_autocomplete',
                                            attrs = {'data-minimum-input-length': 0}))

class SearchAdjectiveForm(SearchForm):
    search_id = forms.ModelChoiceField(label = "Find Adjective:", queryset=Adjective.objects.all(),
                                            widget=autocomplete.ModelSelect2(
                                            url = 'premises:adjectives_autocomplete',
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
        self.helper = FormHelper()
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'


class CategorizationCreateForm(PremiseCreateForm):
    class Meta:
        model = Premise
        fields = ['premise_type', 'key_subject', 'key_object']
        widgets = {
            'key_subject': autocomplete.ModelSelect2(url = 'premises:nouns_autocomplete_create',
                                                     forward = ['key_object']),
            'key_object': autocomplete.ModelSelect2(url = 'premises:nouns_autocomplete_create',
                                                    forward = ['key_subject']),
        }
        labels = {
            'premise_type': 'Type of statement:',
            'key_subject': 'What is being categorized?',
            'key_object': 'Into which category?',
        }

    def __init__(self, *args, **kwargs):
        super(CategorizationCreateForm, self).__init__(*args, **kwargs)
        self.fields['premise_type'].initial = 1
        self.fields['premise_type'].disabled = True
        self.helper.add_input(Submit('submit', 'Categorize'))

    def clean(self):
        cleaned_data = super(CategorizationCreateForm, self).clean()
        key_subject = cleaned_data.get("key_subject")
        key_object = cleaned_data.get("key_object")
        premise_type = cleaned_data.get("premise_type")
        if key_subject and key_object and premise_type:
            if key_subject == key_object:
                raise forms.ValidationError("Cannot categorize into self.")
