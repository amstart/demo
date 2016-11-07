from django.db import models
from django import forms
from django.core.validators import RegexValidator

from demoslogic.blockobjects.models import NetworkObject, VoteBase

class PremiseManager(models.Manager):
    pass
    # def with_counts(self, string = ""):
    #     concatenated = Concat('subject', V(' ('), 'predicate')


class TrimmedCharFormField(forms.CharField):
    def clean(self, value):
        if value:
            value = value.strip()
        return super(TrimmedCharFormField, self).clean(value)


class TrimmedCharField(models.CharField):
    validators=[RegexValidator(regex='^[a-zA-Z ]+$', message='Only letters and spaces allowed.')]

    def formfield(self, **kwargs):
        return super(TrimmedCharField, self).formfield(form_class=TrimmedCharFormField, **kwargs)

class Premise(NetworkObject):
    objects = PremiseManager
    name = 'premise'
    namespace = 'premises'   #this is used for URL namespaces!
    subject = TrimmedCharField(default = '', max_length = 200)
    predicate = TrimmedCharField(default = '', max_length = 200)
    object = TrimmedCharField(default = '', max_length = 200, blank = True)
    complement = TrimmedCharField(default = '', max_length = 200, blank = True)

    def __init__(self, *args, **kwargs):
        super(Premise,self).__init__(*args, **kwargs)
        self.core_list = [{"textclass":"subject", "value":self.subject},
                          {"textclass":"predicate", "value":self.predicate}]
        if len(self.object) > 0:
            self.core_list.append({"textclass":"object", "value":self.object})
        if len(self.complement ) > 0:
            self.core_list.append({"textclass":"complement", "value":self.complement})

    def __str__(self):
        print_raw = self.subject + " " + self.predicate
        if len(self.object) > 0:
            print_raw = print_raw + " " + self.object
        if len(self.complement ) > 0:
            print_raw = print_raw + " " + self.complement
        return print_raw


class Vote(VoteBase):
    object = models.ForeignKey(Premise, on_delete = models.CASCADE)

    class Meta:
        abstract = True

class CategorizationVote(Vote):
    value = models.IntegerField(default = 1,
                                choices = ((1, "Not accurate at all or very little"),
                                           (2, "Barely useful"),
                                           (3, "Useful"),
                                           (4, "Completely accurate")))

#choice has a meta class with the ForeignKey and some API, and the base classes with their specific set of choices
#premises and arguments also might share a meta class
