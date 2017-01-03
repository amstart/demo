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
    search_id = forms.ModelChoiceField(label = "Find QStatement:", queryset =models.Premise.objects.all(),
                                            widget = autocomplete.ModelSelect2(
                                            url = 'premises:autocomplete',
                                            attrs = {'data-minimum-input-length': 0}))

class SearchNounForm(SearchForm):
    search_id = forms.ModelChoiceField(label = "Find Entity:", queryset=models.Noun.objects.all(),
                                            widget=autocomplete.ModelSelect2(
                                            url = 'premises:nouns_autocomplete',
                                            attrs = {'data-minimum-input-length': 0}))
class SearchVerbForm(SearchForm):
    search_id = forms.ModelChoiceField(label = "Find Verb:", queryset=models.Verb.objects.all(),
                                            widget=autocomplete.ModelSelect2(
                                            url = 'premises:verbs_autocomplete',
                                            attrs = {'data-minimum-input-length': 0}))

class SearchAdjectiveForm(SearchForm):
    search_id = forms.ModelChoiceField(label = "Find Attribute:", queryset=models.Adjective.objects.all(),
                                            widget=autocomplete.ModelSelect2(
                                            url = 'premises:adjectives_autocomplete',
                                            attrs = {'data-minimum-input-length': 0}))

class PremiseVoteForm(VoteForm):
    def __init__(self, *args, **kwargs):
        object = kwargs.pop('object', None)
        super(PremiseVoteForm, self).__init__(*args, **kwargs) #loads form helper
        if object:
            self.fields['value'].initial = None
            self.fields['value'].choices = object.get_theses_choices()
            self.fields['value2'].initial = None
            self.fields['value2'].choices = object.get_demands_choices()
            # self.max_choice = object.max_choice

    class Meta:
        model = models.PremiseVote
        fields = ['value', 'value2']
        widgets = {'value': forms.RadioSelect, 'value2': forms.RadioSelect}
        labels = {'value': "Which of these statements do you think gets closest to the truth?",
                  'value2': "Which of these statements reflects your opinion most?"}


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
        self.helper.add_input(Submit('submit', 'Submit'))
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
            'key_object': 'is/should (not) be a type of',
        }


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
            'key_object': 'does/should not/partly/exclusively comprise',
        }


class ComparisonCreateForm(PremiseCreateForm):
    premise_type = settings.TYPE_COMPARISON

    class Meta(PremiseCreateForm.Meta):
        fields = ['premise_type', 'key_subject', 'key_complement', 'key_object', 'key_indirect_object']
        widgets = {
            'key_subject': autocomplete.ModelSelect2(url = 'premises:nouns_autocomplete_create',
                                                     forward = ['key_object']),
            'key_complement': autocomplete.ModelSelect2(url = 'premises:adjectives_autocomplete_create'),
            'key_object': autocomplete.ModelSelect2(url = 'premises:nouns_autocomplete_create',
                                                    forward = ['key_subject']),
            'key_indirect_object': autocomplete.ModelSelect2(url = 'premises:nouns_autocomplete_create'),
        }
        labels = {
            'key_subject': '',
            'key_complement': 'is/should be equally/less/more',
            'key_object': 'as/than',
            'key_indirect_object': 'for (the) [optional]'
        }


class RelationCreateForm(PremiseCreateForm):
    premise_type = settings.TYPE_RELATION

    class Meta(PremiseCreateForm.Meta):
        fields = ['premise_type', 'key_subject', 'key_object', 'key_indirect_object']
        widgets = {
            'key_subject': autocomplete.ModelSelect2(url = 'premises:nouns_autocomplete_create',
                                                     forward = ['key_object']),
            'key_object': autocomplete.ModelSelect2(url = 'premises:nouns_autocomplete_create',
                                                    forward = ['key_subject']),
            'key_indirect_object': autocomplete.ModelSelect2(url = 'premises:nouns_autocomplete_create'),
        }
        labels = {
            'key_subject': 'When there is more',
            'key_object': ', there is/should be more/less/no change in',
            'key_indirect_object': 'for (the) [optional]'
        }

class QuantityCreateForm(PremiseCreateForm):
    premise_type = settings.TYPE_QUANTITY

    class Meta(PremiseCreateForm.Meta):
        fields = ['premise_type', 'key_subject', 'key_indirect_object']
        widgets = {
            'key_subject': autocomplete.ModelSelect2(url = 'premises:nouns_autocomplete_create',
                                                     forward = ['key_indirect_object']),
            'key_indirect_object': autocomplete.ModelSelect2(url = 'premises:nouns_autocomplete_create',
                                                    forward = ['key_subject']),
        }
        labels = {
            'key_subject': 'There is (no)/might be or should be more/less/an equal amount of',
            'key_indirect_object': 'for (the) [optional]'
        }

class EncouragmentCreateForm(PremiseCreateForm):
    premise_type = settings.TYPE_ENCOURAGEMENT

    class Meta(PremiseCreateForm.Meta):
        fields = ['premise_type', 'key_subject', 'key_indirect_object']
        widgets = {
            'key_subject': autocomplete.ModelSelect2(url = 'premises:nouns_autocomplete_create',
                                                     forward = ['key_indirect_object']),
            'key_indirect_object': autocomplete.ModelSelect2(url = 'premises:nouns_autocomplete_create',
                                                    forward = ['key_subject']),
        }
        labels = {
            'key_subject': 'The following is/should be encouraged/discouraged/left alone:',
            'key_indirect_object': 'for (the) [optional]'
        }
