from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django import forms

from .models import Premise, CategorizationVote

class CategorizationVoteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CategorizationVoteForm, self).__init__(*args, **kwargs)
        if self.fields['value'].choices[0][0] == '':
            choices = self.fields['value'].choices
            del choices[0] #get rid of the first empty radio button
            #http://stackoverflow.com/questions/8928565/django-cant-remove-empty-label-from-typedchoicefield#8995937
            self.fields['value'].choices = choices
        self.helper = FormHelper()
        self.helper.form_id = 'id-CategorizationVoteForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = CategorizationVote
        fields = ['value']
        widgets = {'value': forms.RadioSelect}
        labels = {'value': "How accurate do you think this categorization is?"}
        # empty_labels = {'value': None}

class AbstractForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AbstractForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = True
    class Meta:
        abstract = True

class WithComplementedObjectInputForm(AbstractForm):
    class Meta:
        model = Premise
        fields = ['subject', 'predicate', 'object', 'complement']

class WithObjectInputForm(AbstractForm):
    class Meta:
        model = Premise
        fields = ['subject', 'predicate', 'object']

class WithComplementInputForm(AbstractForm):
    class Meta:
        model = Premise
        fields = ['subject', 'predicate', 'complement']

class SubjectPredicateInputForm(AbstractForm):
        class Meta:
            model = Premise
            fields = ['subject', 'predicate']
