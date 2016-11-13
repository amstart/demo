from dal import autocomplete
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Fieldset
from django import forms
from django.db.models import Q

from demoslogic.blockobjects.forms import VoteForm
from demoslogic.premises.models import Premise

from .models import Argument, ArgumentVote


class ArgumentVoteForm(VoteForm):
    class Meta:
        model = ArgumentVote
        fields = ['value']
        widgets = {'value': forms.RadioSelect}
        labels = {'value': "How strong do you think this argument is?"}
        # empty_labels = {'value': None}

class ArgumentInputForm(forms.ModelForm):
    class Meta:
        model = Argument
        fields = ['premise1', 'premise2', 'conclusion', 'aim']
        widgets = {
            'premise1': autocomplete.ModelSelect2(url = 'premises:autocomplete',
                                                  forward = ['premise2', 'conclusion']),
            'premise2': autocomplete.ModelSelect2(url = 'premises:autocomplete',
                                                  forward = ['premise1', 'conclusion']),
            'conclusion': autocomplete.ModelSelect2(url = 'premises:autocomplete',
                                                    forward = ['premise1', 'premise2'])
        }

    def __init__(self, *args, **kwargs):
        super(ArgumentInputForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'

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
