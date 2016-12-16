from django.db import models

from demoslogic.blockobjects.models import NetworkObject, VoteBase
from demoslogic.premises.models import Premise

class Argument(NetworkObject):
    name_lower = 'argument'
    name_upper = 'Argument'
    namespace = 'arguments'   #this is used for URL namespaces!
    premise1_if = models.IntegerField()
    premise1 = models.ForeignKey(Premise, on_delete = models.CASCADE, related_name='premise1')
    premise2_if = models.IntegerField()
    premise2 = models.ForeignKey(Premise, on_delete = models.CASCADE, related_name='premise2')
    aim = models.IntegerField()
    conclusion = models.ForeignKey(Premise, on_delete = models.CASCADE, related_name='conclusion')

    class Meta(NetworkObject.Meta):
        unique_together = ("premise1_if", "premise1", "premise2", "premise2_if",
                           "aim", "conclusion")

    def __init__(self, *args, **kwargs):
        super(Argument,self).__init__(*args, **kwargs)
        if hasattr(self, 'premise1'):
            self.premise1_thesis = self.premise1.get_premise_choice(self.premise1_if)
            self.premise2_thesis = self.premise2.get_premise_choice(self.premise2_if)
            self.conclusion_thesis = self.conclusion.get_premise_choice(self.aim)

    def __str__(self):
        return self.conclusion_thesis

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
