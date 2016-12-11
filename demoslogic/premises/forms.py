from dal import autocomplete
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, HTML

from django import forms
from django.core.urlresolvers import reverse, reverse_lazy

from demoslogic.blockobjects.forms import VoteForm, SearchForm
from . import models, settings

class NewPremiseForm(forms.ModelForm):
    class Meta:
        model = models.Premise
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

class PremiseVoteForm(VoteForm):
    def __init__(self, *args, **kwargs):
        object = kwargs.pop('object', None)
        super(PremiseVoteForm, self).__init__(*args, **kwargs) #loads form helper
        if object:
            self.fields['value'].initial = None
            self.fields['value'].choices = (object.choices)
            # self.max_choice = object.max_choice

    class Meta:
        model = models.PremiseVote
        fields = ['value']
        widgets = {'value': forms.RadioSelect}
        labels = {'value': "How accurate do you think this categorization is?"}

    # def clean_value(self):
    #     value = self.cleaned_data.get("value")
    #     if value > self.max_choice or value < 0:
    #         raise forms.ValidationError("Value not allowed.")
    #     return cleaned_data

class PremiseCreateForm(forms.ModelForm):
    class Meta:
        model = models.Premise
        fields = ['premise_type']

    def clean(self):
        cleaned_data = super(PremiseCreateForm, self).clean()
        premise_type = cleaned_data.get("premise_type")
        premise_type = self.premise_type
        if cleaned_data.get("key_subject", None) == cleaned_data.get("key_object", None):
            raise forms.ValidationError("Same thing twice? Try harder :).")
        return cleaned_data

    def clean_doublets(self, cd):
        premises = models.Premise.objects.filter(premise_type = cd.get("premise_type")) \
                    .filter(key_subject = cd.get("key_subject", None)) \
                    .filter(key_object = cd.get("key_object", None)) \
                    .filter(key_indirect_object = cd.get("key_indirect_object", None)) \
                    .filter(key_complement = cd.get("key_complement", None)) \
                    .filter(key_predicate = cd.get("key_predicate", None))
        if premises.count():
            raise forms.ValidationError("This premise already exists.")
        else:
            return cd

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
            'key_subject': '',
            'key_object': 'is (not) a type of',
        }

    def __init__(self, *args, **kwargs):
        super(CategorizationCreateForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Categorize'))

    def clean(self):
        cleaned_data = super(CategorizationCreateForm, self).clean()
        return cleaned_data

class CollectionCreateForm(PremiseCreateForm):
    premise_type = settings.TYPE_COLLECTION

    class Meta(PremiseCreateForm.Meta):
        fields = ['premise_type', 'key_subject', 'key_object']
        widgets = {
            'key_subject': autocomplete.ModelSelect2(url = 'premises:nouns_autocomplete_create',
                                                     forward = ['key_object']),
            'key_object': autocomplete.ModelSelect2(url = 'premises:nouns_autocomplete_create',
                                                    forward = ['key_subject']),
        }
        labels = {
            'key_subject': '',
            'key_object': 'does not/partly/exclusively comprise',
        }

    def __init__(self, *args, **kwargs):
        super(CollectionCreateForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Collect'))

    def clean(self):
        cleaned_data = super(CollectionCreateForm, self).clean()
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
            'key_subject': '',
            'key_complement': 'is equally/less/more...',
            'key_object': 'as/than:',
            'key_indirect_object': 'for'
        }

    def __init__(self, *args, **kwargs):
        super(ComparisonCreateForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Compare'))

    def clean(self):
        cleaned_data = super(ComparisonCreateForm, self).clean()
        return cleaned_data


class RelationCreateForm(PremiseCreateForm):
    premise_type = settings.TYPE_RELATION

    class Meta(PremiseCreateForm.Meta):
        fields = ['premise_type', 'key_subject', 'key_object']
        widgets = {
            'key_subject': autocomplete.ModelSelect2(url = 'premises:nouns_autocomplete_create',
                                                     forward = ['key_object']),
            'key_object': autocomplete.ModelSelect2(url = 'premises:nouns_autocomplete_create',
                                                    forward = ['key_subject']),
        }
        labels = {
            'key_subject': '',
            'key_object': 'is equally/more/less often thas not accompanied with the following:',
        }

    def __init__(self, *args, **kwargs):
        super(RelationCreateForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Relate'))

    def clean(self):
        cleaned_data = super(RelationCreateForm, self).clean()
        return cleaned_data
