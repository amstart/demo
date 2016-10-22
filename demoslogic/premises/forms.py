from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django import forms

from .models import Premise

class CategorizationVoteForm(forms.Form):
    like_website = forms.TypedChoiceField(label = "How accurate do you think this categorization is?",
                                          choices = ((1, "Not accurate at all or very little"),
                                                     (2, "Barely useful"),
                                                     (3, "Useful"),
                                                     (4, "Completely accurate")),
                                          coerce = lambda x: bool(int(x)),
                                          widget = forms.RadioSelect,
                                          initial = '1',
                                          required = True,)

    def __init__(self, *args, **kwargs):
        super(CategorizationVoteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-CategorizationVoteForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_vote'
        self.helper.add_input(Submit('submit', 'Submit'))


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
