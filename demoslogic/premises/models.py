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
    validators = [RegexValidator(regex='^[a-zA-Z ]+$', message = 'Only letters and spaces allowed.')]

    def formfield(self, **kwargs):
        return super(TrimmedCharField, self).formfield(form_class = TrimmedCharFormField, **kwargs)

class Noun(models.Model):
    name = TrimmedCharField(default = '', max_length = 50)
    def __str__(self):
        return self.name

class Predicate(models.Model):
    name = TrimmedCharField(default = '', max_length = 50)
    def __str__(self):
        return self.name

class Complement(models.Model):
    name = TrimmedCharField(default = '', max_length = 100)
    def __str__(self):
        return self.name

class Premise(NetworkObject):
    objects = PremiseManager
    name_lower = 'statement'
    name_upper = 'Statement'
    namespace = 'premises'   #this is used for URL namespaces!
    sentence = TrimmedCharField(default = '', max_length = 250, blank = True)
    key_subject = models.ForeignKey(Noun, on_delete = models.DO_NOTHING, related_name = 'key_subject')
    key_predicate = models.ForeignKey(Predicate, on_delete = models.DO_NOTHING)
    key_object = models.ForeignKey(Noun, on_delete = models.DO_NOTHING, related_name = 'key_object', null = True)
    key_complement = models.ForeignKey(Complement, on_delete = models.DO_NOTHING, null = True)
    premise_type = models.IntegerField(default = 1,
                                       choices = ((1, "Categorization"),
                                                  (2, "Comparison"),
                                                  (3, "Empirical claim"),
                                                  (4, "Proposal")))

    def save(self, *args, **kwargs):
        self.sentence = str(self.key_subject) + " " + str(self.key_predicate)
        if self.key_object:
            self.sentence = self.sentence + " " + str(self.key_object)
        if self.key_complement:
            self.sentence = self.sentence + " " + str(self.key_complement)
        super(Premise, self).save(*args, **kwargs)

    def __str__(self):
        return self.sentence

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
