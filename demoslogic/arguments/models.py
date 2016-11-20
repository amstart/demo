from django.db import models

from demoslogic.blockobjects.models import NetworkObject, VoteBase
from demoslogic.premises.models import Premise

premise_what = ((1, "If the positive version of the following statement is given:"),
              (2, "If the negative version of the following statement is given:"),
              (3, "If the following affects most people:"),
              (4, "If there is missing knowledge on the following matter:"))

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
    premise1_if = models.IntegerField(default = 1, choices = premise_what)
    premise1 = models.ForeignKey(Premise, on_delete = models.CASCADE, related_name='premise1')
    premise2_if = models.IntegerField(default = 1, choices = premise_what)
    premise2 = models.ForeignKey(Premise, on_delete = models.CASCADE, related_name='premise2')
    conclusion = models.ForeignKey(Premise, on_delete = models.CASCADE, related_name='conclusion')
    aim = models.IntegerField(default = 1,
                              choices = (
                                  (1, "The positive version of the following conclusion is true:"),
                                  (2, "The negative version of the following conclusion is true:"),
                                  (3, "The following is relevant:"),
                                  (4, "The following is irrelevant:"),#needs to take arguments!
                                  (5, "To point out missing knowledge on the matter."))
                              )

    def __init__(self, *args, **kwargs):
        super(Argument,self).__init__(*args, **kwargs)
        self.aim_heading = aim_heading[self.aim-1]
        self.aim_what = aim_what[self.aim-1]
        self.premise1_what = premise_what[self.premise1_if-1][1]
        self.premise2_what = 'And i' + premise_what[self.premise2_if-1][1][1:]

    def __str__(self):
        return self.aim_heading + ': ' + str(self.conclusion)

class Vote(VoteBase):
    object = models.ForeignKey(Argument, on_delete = models.CASCADE)

    class Meta:
        abstract = True

class ArgumentVote(Vote):
    value = models.IntegerField(default = 1,
                                choices = ((1, "completely invalid"),
                                           (2, "weak"),
                                           (3, "strong"),
                                           (4, "completely valid")))
