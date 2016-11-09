from dal import autocomplete
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django import forms

from demoslogic.premises.models import Premise

class VoteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(VoteForm, self).__init__(*args, **kwargs)
        if self.fields['value'].choices[0][0] == '':
            choices = self.fields['value'].choices
            del choices[0] #get rid of the first empty radio button
            #http://stackoverflow.com/questions/8928565/django-cant-remove-empty-label-from-typedchoicefield#8995937
            self.fields['value'].choices = choices
        self.helper = FormHelper()
        self.helper.form_id = 'id-VoteForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

class SearchPremiseForm(forms.Form):
    premise_search = forms.ModelChoiceField(label = "", queryset=Premise.objects.all(),
                                            widget=autocomplete.ModelSelect2(
                                            url = 'premises:autocomplete',))
                                            # attrs = {'data-minimum-input-length': 3}))
    # search = forms.CharField()
    # class Meta:
    #     widgets = {
    #         'search': autocomplete.ModelSelect2(url = reverse_lazy('premises:autocomplete'))}
