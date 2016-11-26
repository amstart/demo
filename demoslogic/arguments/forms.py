from dal import autocomplete
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Fieldset
from django import forms
from django.db.models import Q
from django.core.urlresolvers import reverse, reverse_lazy

from demoslogic.blockobjects.forms import VoteForm
from demoslogic.premises.models import Premise
from .models import Argument, ArgumentVote


class NewArgumentForm(forms.ModelForm):
    class Meta:
        model = Argument
        fields = ['premise1', 'premise2', 'conclusion']
        widgets = {
            'premise1': autocomplete.ModelSelect2(url = 'premises:autocomplete',
                                                  forward = ['premise2', 'conclusion']),
            'premise2': autocomplete.ModelSelect2(url = 'premises:autocomplete',
                                                  forward = ['premise1', 'conclusion']),
            'conclusion': autocomplete.ModelSelect2(url = 'premises:autocomplete',
                                                    forward = ['premise1', 'premise2'])
        }

    def __init__(self, *args, **kwargs):
        super(NewArgumentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.form_action = reverse_lazy('arguments:create')
        self.helper.add_input(Submit('submit', 'Choose'))


class ArgumentVoteForm(VoteForm):
    def __init__(self, *args, **kwargs):
        super(ArgumentVoteForm, self).__init__(*args, **kwargs)
        if self.fields['value'].choices[0][0] == '':
            choices = self.fields['value'].choices
            choices[0][1] = "Undecided"
            del choices[0] #get rid of the first empty radio button
            #http://stackoverflow.com/questions/8928565/django-cant-remove-empty-label-from-typedchoicefield#8995937
            self.fields['value'].choices = choices


    class Meta:
        model = ArgumentVote
        fields = ['value']
        widgets = {'value': forms.RadioSelect}
        labels = {'value': "How strong do you think this argument is?"}
        # empty_labels = {'value': None}

class ArgumentCreateForm(forms.ModelForm):
    class Meta:
        model = Argument
        fields = ['premise1_if', 'premise2_if', 'aim']
        labels = {'premise1_if': "", 'premise2_if': "", 'aim': ""}

    def __init__(self, *args, **kwargs):
        super(ArgumentCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Argue'))
        choice_default = ((0, 'Select Statement first'),
                          (0, 'You need to select a statement first for proper choices to appear here.'))
        self.fields['premise1_if'].widget = forms.Select(choices = choice_default)
        self.fields['premise1_if'].intial = 0

    def clean(self):
        cleaned_data = super(ArgumentInputForm, self).clean()
        premise1 = cleaned_data.get("premise1")
        premise2 = cleaned_data.get("premise2")
        conclusion = cleaned_data.get("conclusion")
        aim = cleaned_data.get("aim")
        if premise1 and premise2 and conclusion:
            # Only do something if all fields are valid so far.
            if premise1 == premise2 or premise1 == conclusion or premise2 == conclusion:
                raise forms.ValidationError("A premise can only be used once per argument.")
        arguments = Argument.objects.filter(conclusion = conclusion) \
                    .filter(Q(premise1 = premise1) | Q(premise1 = premise2)) \
                    .filter(Q(premise2 = premise1) | Q(premise2 = premise2)) \
                    .filter(aim = aim)
        if arguments.count():
            raise forms.ValidationError("This argument already exists.")
