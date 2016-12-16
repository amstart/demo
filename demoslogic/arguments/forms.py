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
        object = kwargs.pop('object', None)
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
        fields = ['premise1', 'premise1_if', 'premise2', 'premise2_if', 'conclusion', 'aim',]
        labels = {'premise1_if': "", 'premise1': "", 'premise2_if': "",
                  'premise2': "", 'aim': "", 'conclusion': ""}

    def __init__(self, *args, **kwargs):
        premise1 = Premise.objects.get(pk = kwargs.pop('premise1', None))
        premise2 = Premise.objects.get(pk = kwargs.pop('premise2', None))
        conclusion = Premise.objects.get(pk = kwargs.pop('conclusion', None))
        super(ArgumentCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Argue'))
        if premise1:
            self.fields['premise1'].initial = premise1
            self.fields['premise2'].initial = premise2
            self.fields['conclusion'].initial = conclusion
            self.fields['premise1'].widget.attrs['readonly'] = 'readonly'
            self.fields['premise2'].widget.attrs['readonly'] = 'readonly'
            self.fields['conclusion'].widget.attrs['readonly'] = 'readonly'
            self.fields['premise1'].widget.attrs['onChange'] = "window.location='" + reverse("arguments:new") + "'"
            self.fields['premise2'].widget.attrs['onChange'] = "window.location='" + reverse("arguments:new") + "'"
            self.fields['conclusion'].widget.attrs['onChange'] = "window.location='" + reverse("arguments:new") + "'"
            self.fields['premise1_if'].widget = forms.Select(choices = premise1.get_argument_choices())
            self.fields['premise1_if'].initial = 0
            self.fields['premise2_if'].widget = forms.Select(choices = [(0, 'Choose')] + \
                                                             premise2.get_argument_choices())
            self.fields['premise2_if'].initial = 0
            self.fields['aim'].widget = forms.Select(choices = [(0, 'Choose')] + conclusion.get_argument_choices())
            self.fields['aim'].initial = 0

    def clean(self):
        cleaned_data = super(ArgumentCreateForm, self).clean()
        premise1_if = cleaned_data.get("premise1_if")
        premise2_if = cleaned_data.get("premise2_if")
        aim = cleaned_data.get("aim")
        if aim == 0 or premise1_if == 0 or premise2_if == 0:
            raise forms.ValidationError("Choose a thesis for your statements.")
        premise1 = cleaned_data.get("premise1")
        premise2 = cleaned_data.get("premise2")
        conclusion = cleaned_data.get("conclusion")
        aim = cleaned_data.get("aim")
        if premise1 and premise2 and conclusion:
            # Only do something if all fields are valid so far.
            if premise1 == premise2 or premise1 == conclusion or premise2 == conclusion:
                raise forms.ValidationError("A premise can only be used once per argument.")
        arguments = Argument.objects.filter(conclusion = conclusion).filter(aim = aim) \
                    .filter((Q(premise1 = premise1) & Q(premise1_if = premise1_if)) | \
                            (Q(premise1 = premise2)) & Q(premise1_if = premise2_if)) \
                    .filter((Q(premise2 = premise1) & Q(premise2_if = premise1_if)) | \
                            (Q(premise2 = premise2)) & Q(premise2_if = premise2_if))
        if arguments.count():
            raise forms.ValidationError("This argument already exists.")
