from .models import Choice, Premise
from django import forms

class PremiseFullInputForm(forms.ModelForm):
    class Meta:
        model = Premise
        fields = ['subject', 'predicate', 'object', 'complement']

class PremiseWithObjectInputForm(forms.ModelForm):
    class Meta:
        model = Premise
        fields = ['subject', 'predicate', 'object']

class PremiseMinimumInputForm(forms.ModelForm):
    class Meta:
        model = Premise
        fields = ['subject', 'predicate', 'complement']
