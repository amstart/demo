from dal import autocomplete

from django import forms
from django.core.urlresolvers import reverse, reverse_lazy

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

class AbstractForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AbstractForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = True
    class Meta:
        abstract = True

class ArgumentInputForm(AbstractForm):
    class Meta:
        model = Argument
        fields = ['premise1', 'premise2', 'conclusion', 'aim']
        widgets = {
            'premise1': autocomplete.ModelSelect2(url = reverse_lazy('arguments:autocomplete')),
            'premise2': autocomplete.ModelSelect2(url = reverse_lazy('arguments:autocomplete')),
            'conclusion': autocomplete.ModelSelect2(url = reverse_lazy('arguments:autocomplete'))
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
