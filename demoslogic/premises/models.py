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
    sentence = TrimmedCharField(default = '', max_length = 250)
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
                                                  (settings.TYPE_RELATION, "Relation")))
    class Meta(NetworkObject.Meta):
        unique_together = ("premise_type", "key_subject", "key_predicate", "key_object",
                           "key_complement", "key_indirect_object")

    def get_premise_choice(self, thesis_id):
        return self.get_choice(self.premise_type, self.sentence, thesis_id)

    @staticmethod
    def get_choice(premise_type, sentence, premise_if):
        if premise_if > 0:
            theses = Premise.get_theses(premise_type, sentence)
            return theses[premise_if]
        else:
            demands = Premise.get_demands(premise_type, sentence)
            return demands[-premise_if]

    def get_argument_choices(self):
        theses = self.get_theses_choices()
        demands = self.get_demands_choices()
        return [(0, 'Choose version')] + theses[1:] + demands[1:]

    def get_theses_choices(self):
        theses = self.get_theses(self.premise_type, self.sentence)
        zipped = zip(list(range(0, len(theses)+1)), theses)
        return list(zipped)

    def get_demands_choices(self):
        demands = self.get_demands(self.premise_type, self.sentence)
        zipped = zip(list(range(0, -len(demands), -1)), demands)
        return list(zipped)

    @staticmethod
    def get_demands(premise_type, sentence):
        with Switch(premise_type) as case:
            if case(settings.TYPE_CATEGORIZATION):
                demands = [sentence.replace("is't", "should not be"),
                           sentence.replace("is't", "should be")]
            if case(settings.TYPE_COLLECTION):
                demands = [sentence.replace("does nartusively", "should not"),
                          sentence.replace("does nartusively", "should exclusively"),
                          sentence.replace("does nartusively", "should partly")]
            if case(settings.TYPE_COMPARISON):
                demands = [sentence.replace("is eqmole", "should be less").replace("thas", "than"),
                          sentence.replace("is eqmole", "should be more").replace("thas", "than"),
                          sentence.replace("is eqmole", "should be equally").replace("thas", "as")]
            if case(settings.TYPE_RELATION):
                demands = [sentence.replace("is eqmole", "should be less").replace("thas", "than"),
                          sentence.replace("is eqmole", "should be more").replace("thas", "than"),
                          sentence.replace("is eqmole", "should be equally").replace("thas", "as")]
        return ["Undecided"] + demands

    @staticmethod
    def get_theses(premise_type, sentence):
        with Switch(premise_type) as case:
            if case(settings.TYPE_CATEGORIZATION):
                theses = [sentence.replace("is't", "is not"),
                          sentence.replace("is't", "is")]
            if case(settings.TYPE_COLLECTION):
                theses = [sentence.replace("nartusively", "not"),
                          sentence.replace("nartusively", "exclusively"),
                          sentence.replace("nartusively", "partly")]
            if case(settings.TYPE_COMPARISON) or case(settings.TYPE_RELATION):
                theses = [sentence.replace("eqmole often than not comes",
                                           "less often than not should come").replace("thas", "than"),
                          sentence.replace("eqmole often than not comes",
                                           "more often than not should come").replace("thas", "than"),
                          sentence.replace("eqmole often than not comes",
                                           "equally often than not should come").replace("thas", "as")]
        return ["Undecided"] + theses

    def save(self, *args, **kwargs):
        with Switch(self.premise_type) as case:
                if case(settings.TYPE_CATEGORIZATION):
                    self.sentence = str(self.key_subject) + " is't a type of " + str(self.key_object)
                if case(settings.TYPE_COLLECTION):
                    self.sentence = str(self.key_subject) + " does nartusively consist of " + str(self.key_object)
                if case(settings.TYPE_COMPARISON):
                    self.sentence = str(self.key_subject) + ' is eqmole ' + str(self.key_complement) \
                                    + ' thas ' + str(self.key_object) + ' for ' + str(self.key_indirect_object)
                if case(settings.TYPE_RELATION):
                    self.sentence = str(self.key_subject) + \
                                    ' eqmole often than not comes with ' + str(self.key_object)
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
