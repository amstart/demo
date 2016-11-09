from dal import autocomplete

from django import forms

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

    def clean(self):
        cleaned_data = super(ArgumentInputForm, self).clean()
        premise1 = cleaned_data.get("premise1")
        premise2 = cleaned_data.get("premise2")
        conclusion = cleaned_data.get("conclusion")
        if premise1 and premise2 and conclusion:
            # Only do something if all fields are valid so far.
            if premise1 == premise2 or premise1 == conclusion or premise2 == conclusion:
                raise forms.ValidationError("A premise can only be used once per argument.")
