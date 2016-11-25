from dal import autocomplete
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, HTML

from django import forms
from django.core.urlresolvers import reverse, reverse_lazy

from demoslogic.blockobjects.forms import VoteForm, SearchForm
from . import models, settings

class NewPremiseForm(forms.ModelForm):
    class Meta:
        model =models.Premise
        fields = ['premise_type']
        labels = {'premise_type': "Which type?"}

    def __init__(self, *args, **kwargs):
        super(NewPremiseForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.form_action = reverse_lazy('premises:create')
        self.helper.add_input(Submit('submit', 'Choose'))


class SearchPremiseForm(SearchForm):
    search_id = forms.ModelChoiceField(label = "Find Statement:", queryset =models.Premise.objects.all(),
                                            widget = autocomplete.ModelSelect2(
                                            url = 'premises:autocomplete',
                                            attrs = {'data-minimum-input-length': 0}))

class SearchNounForm(SearchForm):
    search_id = forms.ModelChoiceField(label = "Find Noun:", queryset=models.Noun.objects.all(),
                                            widget=autocomplete.ModelSelect2(
                                            url = 'premises:nouns_autocomplete',
                                            attrs = {'data-minimum-input-length': 0}))
class SearchVerbForm(SearchForm):
    search_id = forms.ModelChoiceField(label = "Find Verb:", queryset=models.Verb.objects.all(),
                                            widget=autocomplete.ModelSelect2(
                                            url = 'premises:verbs_autocomplete',
                                            attrs = {'data-minimum-input-length': 0}))

class SearchAdjectiveForm(SearchForm):
    search_id = forms.ModelChoiceField(label = "Find Adjective:", queryset=models.Adjective.objects.all(),
                                            widget=autocomplete.ModelSelect2(
                                            url = 'premises:adjectives_autocomplete',
                                            attrs = {'data-minimum-input-length': 0}))

class CategorizationVoteForm(VoteForm):
    def __init__(self, *args, **kwargs):
        super(CategorizationVoteForm, self).__init__(*args, **kwargs)
        choices = self.fields['value'].choices
        choices[1][1] = "sdfsd"
        self.fields['value'].choices = choices

    class Meta:
        model = models.CategorizationVote
        fields = ['value']
        widgets = {'value': forms.RadioSelect}
        labels = {'value': "How accurate do you think this categorization is?"}
        # empty_labels = {'value': None}


class PremiseCreateForm(forms.ModelForm):
    class Meta:
        model = models.Premise
        fields = ['premise_type']

    def clean(self):
        cleaned_data = super(PremiseCreateForm, self).clean()
        print(cleaned_data)
        premise_type = cleaned_data.get("premise_type")
        premise_type = self.premise_type
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(PremiseCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.fields['premise_type'].initial = self.premise_type
        self.fields['premise_type'].label = 'Type of statement:'
        self.fields['premise_type'].widget.attrs['readonly'] = 'readonly'
        self.fields['premise_type'].widget.attrs['onChange'] = "window.location='" + reverse("premises:new") + "'"


class CategorizationCreateForm(PremiseCreateForm):
    premise_type = settings.TYPE_CATEGORIZATION

    class Meta(PremiseCreateForm.Meta):
        fields = ['premise_type', 'key_subject', 'key_object']
        widgets = {
            'key_subject': autocomplete.ModelSelect2(url = 'premises:nouns_autocomplete_create',
                                                     forward = ['key_object']),
            'key_object': autocomplete.ModelSelect2(url = 'premises:nouns_autocomplete_create',
                                                    forward = ['key_subject']),
        }
        labels = {
            'key_subject': 'What is being categorized?',
            'key_object': 'Into which category?',
        }

    def __init__(self, *args, **kwargs):
        super(CategorizationCreateForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Categorize'))

    def clean(self):
        cleaned_data = super(CategorizationCreateForm, self).clean()
        print(cleaned_data)
        key_subject = cleaned_data.get("key_subject")
        key_object = cleaned_data.get("key_object")
        if key_subject and key_object:
            if key_subject == key_object:
                raise forms.ValidationError("Cannot categorize into self.")
        return cleaned_data

class ComparisonCreateForm(PremiseCreateForm):
    premise_type = settings.TYPE_COMPARISON

    class Meta(PremiseCreateForm.Meta):
        fields = ['premise_type', 'key_subject', 'key_complement', 'key_object', 'key_indirect_object']
        widgets = {
            'key_subject': autocomplete.ModelSelect2(url = 'premises:nouns_autocomplete_create',
                                                     forward = ['key_object', 'key_indirect_object']),
            'key_complement': autocomplete.ModelSelect2(url = 'premises:adjectives_autocomplete_create'),
            'key_object': autocomplete.ModelSelect2(url = 'premises:nouns_autocomplete_create',
                                                    forward = ['key_subject', 'key_indirect_object']),
            'key_indirect_object': autocomplete.ModelSelect2(url = 'premises:nouns_autocomplete_create',
                                                    forward = ['key_subject', 'key_object']),
        }
        labels = {
            'key_subject': 'What entity is being compared?',
            'key_complement': 'It is less/more...',
            'key_object': 'than:',
            'key_indirect_object': 'for'
        }

    def __init__(self, *args, **kwargs):
        super(ComparisonCreateForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Compare'))

    def clean(self):
        cleaned_data = super(ComparisonCreateForm, self).clean()
        key_subject = cleaned_data.get("key_subject")
        key_object = cleaned_data.get("key_object")
        key_indirect_object = cleaned_data.get("key_indirect_object")
        key_complement = cleaned_data.get("key_complement")
        if key_subject and key_object and key_indirect_object and key_complement:
            if key_subject == key_object:
                raise forms.ValidationError("Cannot compare with self.")
        return cleaned_data
