from .models import Choice, Premise
from django import forms

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
