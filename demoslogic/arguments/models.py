from django.db import models

from demoslogic.blockobjects.models import BlockObject, VoteBase
from demoslogic.premises.models import Premise

class Argument(BlockObject):
    name = 'argument'   #this is used for URL namespaces alongside the class name!
    premise1 = models.ForeignKey(Premise, on_delete = models.CASCADE, related_name='premise1')
    premise2 = models.ForeignKey(Premise, on_delete = models.CASCADE, related_name='premise2')
    conclusion = models.ForeignKey(Premise, on_delete = models.CASCADE, related_name='conclusion')
    aim = models.IntegerField(default = 1,
                              choices = ((1, "To support the positive version of the conclusion."),
                                         (2, "To support the negative version of the conclusion."),
                                         (3, "To point why the conclusion should be resolved soon, if possible."),
                                         (4, "To point out missing knowledge on the matter.")))
    choice_headings = ("Pro",
                       "Contra",
                       "Decision required",
                       "Unknowns")

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
