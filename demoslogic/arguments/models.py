from django.db import models

from demoslogic.blockobjects.models import NetworkObject, VoteBase
from demoslogic.premises.models import Premise

aim_heading = ("Pro",
               "Contra",
               "Decision required",
               "Unknowns")

aim_what = ("The negative version of the following is correct",
                "The positive version of the following is correct",
                "The following conclusion needs to be resolved soon",
                "Humility might be advised upon voting on the following")

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

    def __init__(self, *args, **kwargs):
        super(Argument,self).__init__(*args, **kwargs)
        if hasattr(self, 'premise1'):
            self.premise1_what = self.premise1.theses[self.premise1_if]
            self.premise2_what = self.premise2.theses[self.premise2_if]
            self.conclusion_what = self.conclusion.theses[self.aim]

    def __str__(self):
        return self.conclusion_what

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
