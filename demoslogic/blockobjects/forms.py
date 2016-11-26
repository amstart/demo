from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django import forms

class VoteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(VoteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

class SearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'blueForms'
        self.helper.form_action = ''
        self.helper.form_method = 'get'
        self.helper.add_input(Submit('submit', 'go to'))
