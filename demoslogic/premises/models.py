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
    sentence = models.CharField(default = '', max_length = 250)
    key_subject = models.ForeignKey(Noun, on_delete = models.CASCADE, related_name = 'key_subject')
    key_predicate = models.ForeignKey(Verb, on_delete = models.CASCADE, null = True)
    key_object = models.ForeignKey(Noun, on_delete = models.CASCADE, related_name = 'key_object', null = True)
    key_indirect_object = models.ForeignKey(Noun, on_delete = models.CASCADE,
                                            related_name = 'key_indirect_object', null = True, blank = True)
    key_complement = models.ForeignKey(Adjective, on_delete = models.CASCADE, null = True)
    premise_type = models.IntegerField(default = settings.TYPE_CATEGORIZATION,
                                       choices = ((settings.TYPE_CATEGORIZATION, "Categorization"),
                                                  (settings.TYPE_COLLECTION, "Collection"),
                                                  (settings.TYPE_COMPARISON, "Comparison"),
                                                  (settings.TYPE_RELATION, "Correlation"),
                                                  (settings.TYPE_QUANTITY, "Existence"),
                                                  (settings.TYPE_ENCOURAGEMENT, "Encouragment")))
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
                out = Premise.get_list(premise_type, sentence, "should not be", "should be")
            if case(settings.TYPE_COLLECTION):
                out = Premise.get_list(premise_type, sentence, "should not", "should exclusively", "should partly")
            if case(settings.TYPE_COMPARISON):
                out = Premise.get_list(premise_type, sentence, "should be less", "should be more", "should be equally")
            if case(settings.TYPE_RELATION):
                out = Premise.get_list(premise_type, sentence, "should be less", "should be more",
                                       "should be no change in")
            if case(settings.TYPE_QUANTITY):
                out = Premise.get_list(premise_type, sentence, "should be less", "should be more",
                                       "might be an equal amount of")
            if case(settings.TYPE_ENCOURAGEMENT):
                out = Premise.get_list(premise_type, sentence, "should be discouraged", "should be encouraged",
                                          "should neither be encouraged nor discouraged")
        return ["Undecided"] + out

    @staticmethod
    def get_theses(premise_type, sentence):
        with Switch(premise_type) as case:
            if case(settings.TYPE_CATEGORIZATION):
                out = Premise.get_list(premise_type, sentence, "is not", "is")
            if case(settings.TYPE_COLLECTION):
                out = Premise.get_list(premise_type, sentence, "does not", "does exclusively", "does partly")
            if case(settings.TYPE_COMPARISON):
                out = Premise.get_list(premise_type, sentence, "is less", "is more", "is equally")
            if case(settings.TYPE_RELATION):
                out = Premise.get_list(premise_type, sentence, "is less", "is more", "is no change in")
            if case(settings.TYPE_QUANTITY):
                out = Premise.get_list(premise_type, sentence, "is no", "is", "might be")
            if case(settings.TYPE_ENCOURAGEMENT):
                out = Premise.get_list(premise_type, sentence, "is discouraged", "is encouraged",
                                          "is neither encouraged nor discouraged")
        return ["Undecided"] + out

    @staticmethod
    def get_regexpr(premise_type):
        with Switch(premise_type) as case:
                if case(settings.TYPE_CATEGORIZATION):
                    return "is ?"
                if case(settings.TYPE_COLLECTION):
                    return "does partly ?"
                if case(settings.TYPE_COMPARISON):
                    return "is equally ?"
                if case(settings.TYPE_RELATION):
                    return "is no change in ?"
                if case(settings.TYPE_QUANTITY):
                    return "is ?"
                if case(settings.TYPE_ENCOURAGEMENT):
                    return "is neither encouraged nor discouraged ?"

    @staticmethod
    def get_list(premise_type, sentence, *replace_strings):
        regexpr = Premise.get_regexpr(premise_type)
        sentence_list = []
        for index, r_string in enumerate(replace_strings):
            if index < 2:
                s = sentence.replace(" as ", " than ")
            else:
                s = sentence
            sentence_list.append(s.replace(regexpr, r_string))
        return sentence_list

    def save(self, *args, **kwargs):
        with Switch(self.premise_type) as case:
                if case(settings.TYPE_CATEGORIZATION):
                    self.sentence = str(self.key_subject) + " is ? a type of " + str(self.key_object)
                if case(settings.TYPE_COLLECTION):
                    self.sentence = str(self.key_subject) + " does partly ? consist of " \
                                    + str(self.key_object)
                if case(settings.TYPE_COMPARISON):
                    self.sentence = str(self.key_subject) + ' is equally ? ' + str(self.key_complement) \
                                    + ' as ' + str(self.key_object)
                if case(settings.TYPE_RELATION):
                    self.sentence = 'When there is more ' + str(self.key_subject) + \
                                    ', there is no change in ? ' + str(self.key_object)
                if case(settings.TYPE_QUANTITY):
                    self.sentence = 'There is ? ' + str(self.key_subject)
                if case(settings.TYPE_ENCOURAGEMENT):
                    self.sentence = 'The following is neither encouraged nor discouraged ?: ' + str(self.key_subject)
        if self.key_indirect_object:
            self.sentence = self.sentence + ' for (the) ' + str(self.key_indirect_object)
        super(Premise, self).save(*args, **kwargs)

    def __str__(self):
        return self.sentence

class Vote(VoteBase):
    object = models.ForeignKey(Premise, on_delete = models.CASCADE)

    class Meta:
        abstract = True

class PremiseVote(Vote):
    value = models.IntegerField()
    value2 = models.IntegerField()

#choice has a meta class with the ForeignKey and some API, and the base classes with their specific set of choices
#premises and arguments also might share a meta class
