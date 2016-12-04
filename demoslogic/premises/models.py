from switch import Switch

from django.db import models
from django import forms
from django.core.validators import RegexValidator

from demoslogic.blockobjects.models import NetworkObject, VoteBase

from . import settings

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
    validators = [RegexValidator(regex='^[a-zA-Z ]+$', message = 'Only letters and spaces allowed.')]

    def formfield(self, **kwargs):
        return super(TrimmedCharField, self).formfield(form_class = TrimmedCharFormField, **kwargs)

class Noun(models.Model):
    name = TrimmedCharField(default = '', max_length = 50, unique = True)
    def __str__(self):
        return self.name

class Verb(models.Model):
    name = TrimmedCharField(default = '', max_length = 50, unique = True)
    def __str__(self):
        return self.name

class Adjective(models.Model):
    name = TrimmedCharField(default = '', max_length = 100, unique = True)
    def __str__(self):
        return self.name

class Premise(NetworkObject):
    objects = PremiseManager
    name_lower = 'statement'
    name_upper = 'Statement'
    namespace = 'premises'   #this is used for URL namespaces!
    sentence = TrimmedCharField(default = '', max_length = 250, unique = True)
    key_subject = models.ForeignKey(Noun, on_delete = models.DO_NOTHING, related_name = 'key_subject')
    key_predicate = models.ForeignKey(Verb, on_delete = models.DO_NOTHING, null = True)
    key_object = models.ForeignKey(Noun, on_delete = models.DO_NOTHING, related_name = 'key_object', null = True)
    key_indirect_object = models.ForeignKey(Noun, on_delete = models.DO_NOTHING,
                                            related_name = 'key_indirect_object', null = True)
    key_complement = models.ForeignKey(Adjective, on_delete = models.DO_NOTHING, null = True)
    premise_type = models.IntegerField(default = settings.TYPE_CATEGORIZATION,
                                       choices = ((settings.TYPE_CATEGORIZATION, "Categorization"),
                                                  (settings.TYPE_COLLECTION, "Collection"),
                                                  (settings.TYPE_COMPARISON, "Comparison"),
                                                  (settings.TYPE_DEDUCTION, "Deduction"),
                                                  (settings.TYPE_DIAGNOSIS, "Diagnosis"),
                                                  (settings.TYPE_PROPOSAL, "Proposal")))
    class Meta(NetworkObject.Meta):
        unique_together = ("premise_type", "key_subject", "key_predicate", "key_object",
                           "key_complement", "key_indirect_object")

    def __init__(self, *args, **kwargs):
        super(Premise,self).__init__(*args, **kwargs)
        with Switch(self.premise_type) as case:
            if case(settings.TYPE_CATEGORIZATION):
                theses = [self.sentence.replace("is't", "is not"),
                          self.sentence.replace("is't", "is")]
            if case(settings.TYPE_COLLECTION):
                theses = [self.sentence.replace("nartlusively", "not"),
                          self.sentence.replace("nartlusively", "exclusively"),
                          self.sentence.replace("nartlusively", "partly")]
            if case(settings.TYPE_COMPARISON):
                theses = [self.sentence.replace("eqmole", "less").replace("thas", "than"),
                          self.sentence.replace("eqmole", "more").replace("thas", "than"),
                          self.sentence.replace("eqmole", "equally").replace("thas", "as")]
        self.theses = ["Undecided"] + theses
        self.max_choice = len(self.theses)+1
        zipped = zip(list(range(0, self.max_choice)), self.theses)
        self.choices = list(zipped)

    def save(self, *args, **kwargs):
        with Switch(self.premise_type) as case:
                if case(settings.TYPE_CATEGORIZATION):
                    self.sentence = str(self.key_subject) + " is't a type of " + str(self.key_object)
                if case(settings.TYPE_COLLECTION):
                    self.sentence = str(self.key_subject) + " does nartlusively consist of " + str(self.key_object)
                if case(settings.TYPE_COMPARISON):
                    self.sentence = str(self.key_subject) + ' is eqmole ' + str(self.key_complement) \
                                    + ' thas ' + str(self.key_object) + ' for ' + str(self.key_indirect_object)
        super(Premise, self).save(*args, **kwargs)

    def __str__(self):
        return self.sentence

class Vote(VoteBase):
    object = models.ForeignKey(Premise, on_delete = models.CASCADE)

    class Meta:
        abstract = True

class PremiseVote(Vote):
    value = models.IntegerField()

#choice has a meta class with the ForeignKey and some API, and the base classes with their specific set of choices
#premises and arguments also might share a meta class
