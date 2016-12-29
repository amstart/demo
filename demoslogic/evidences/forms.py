from dal import autocomplete
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, HTML

from django import forms
from django.core.urlresolvers import reverse, reverse_lazy

from demoslogic.blockobjects.forms import VoteForm, SearchForm
from demoslogic.premises.models import Premise
from . import models

class EvidenceVoteForm(VoteForm):
    def __init__(self, *args, **kwargs):
        object = kwargs.pop('object', None)
        super(EvidenceVoteForm, self).__init__(*args, **kwargs)
        if self.fields['value'].choices[0][0] == '':
            choices = self.fields['value'].choices
            choices[0][1] = "Undecided"
            del choices[0] #get rid of the first empty radio button
            #http://stackoverflow.com/questions/8928565/django-cant-remove-empty-label-from-typedchoicefield#8995937
            self.fields['value'].choices = choices

    class Meta:
        model = models.EvidenceVote
        fields = ['value']
        widgets = {'value': forms.RadioSelect}
        labels = {'value': "How relevant and trustworthy do you think the evidence is?"}


class EvidenceCreateForm(forms.ModelForm):
    class Meta:
        model = models.Evidence
        fields = ['statement', 'version', 'URL']
        labels = {'statement': 'Statement',
                  'URL': 'URL', 'version': "Which version of the statement does the evidence support?"}

    def __init__(self, *args, **kwargs):
        statement = Premise.objects.get(pk = kwargs.pop('statement'))
        super(EvidenceCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Support'))
        if statement:
            self.fields['statement'].initial = statement
            self.fields['statement'].widget.attrs['readonly'] = 'readonly'
            self.fields['version'].widget = forms.Select(choices = statement.get_argument_choices())
            self.fields['version'].initial = 0
