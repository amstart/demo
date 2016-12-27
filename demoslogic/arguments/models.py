from django.db import models

from demoslogic.blockobjects.models import NetworkObject, VoteBase
from demoslogic.premises.models import Premise

class Argument(NetworkObject):
    name_lower = 'argument'
    name_upper = 'Argument'
    namespace = 'arguments'   #this is used for URL namespaces!
    premise1_if = models.IntegerField()
    premise1 = models.ForeignKey(Premise, on_delete = models.CASCADE, related_name='premise1')
    premise2_if = models.IntegerField(null = True, default = None)
    premise2 = models.ForeignKey(Premise, on_delete = models.CASCADE, related_name='premise2', null = True,
                                 blank = True, default = None)
    premise3_if = models.IntegerField(null = True, default = None)
    premise3 = models.ForeignKey(Premise, on_delete = models.CASCADE, related_name='premise3', null = True,
                                 blank = True, default = None)
    aim = models.IntegerField()
    conclusion = models.ForeignKey(Premise, on_delete = models.CASCADE, related_name='conclusion')
    sentence = models.CharField(default = '', max_length = 750)

    class Meta(NetworkObject.Meta):
        unique_together = ("premise1_if", "premise1", "premise2", "premise2_if",
                           "aim", "conclusion")

    def __init__(self, *args, **kwargs):
        super(Argument,self).__init__(*args, **kwargs)
        if hasattr(self, 'premise1'):
            self.premise1_thesis = self.premise1.get_premise_choice(self.premise1_if)
            if self.premise2:
                self.premise2_thesis = self.premise2.get_premise_choice(self.premise2_if)
            if self.premise3:
                self.premise3_thesis = self.premise3.get_premise_choice(self.premise3_if)
            self.conclusion_thesis = self.conclusion.get_premise_choice(self.aim)

    def save(self, *args, **kwargs):
        self.sentence = 'IF ' + self.premise1.get_premise_choice(self.premise1_if)
        if self.premise2:
            self.sentence = self.sentence + '<br>AND ' + self.premise2.get_premise_choice(self.premise2_if)
        if self.premise3:
            self.sentence = self.sentence + '<br>AND ' + self.premise3.get_premise_choice(self.premise3_if)
        self.sentence = self.sentence + '<br>THEN ' + self.conclusion.get_premise_choice(self.aim)
        super(Argument, self).save(*args, **kwargs)

    def __str__(self):
        return self.sentence

class Vote(VoteBase):
    object = models.ForeignKey(Argument, on_delete = models.CASCADE)

    class Meta:
        abstract = True

class ArgumentVote(Vote):
    value = models.IntegerField(default = 1,
                                choices = ((0, "completely invalid"),
                                           (1, "weak"),
                                           (2, "strong"),
                                           (3, "completely valid")))
