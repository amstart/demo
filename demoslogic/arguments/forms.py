from django import forms

from demoslogic.blockobjects.forms import VoteForm

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
