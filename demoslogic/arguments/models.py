from django.db import models

from demoslogic.blockobjects.models import NetworkObject, VoteBase
from demoslogic.premises.models import Premise


class Argument(NetworkObject):
    name = 'argument'
    namespace = 'arguments'   #this is used for URL namespaces!
    premise1 = models.ForeignKey(Premise, on_delete = models.CASCADE, related_name='premise1')
    premise2 = models.ForeignKey(Premise, on_delete = models.CASCADE, related_name='premise2')
    conclusion = models.ForeignKey(Premise, on_delete = models.CASCADE, related_name='conclusion')
    aim = models.IntegerField(default = 1,
                              choices = ((1, "To support the positive version of the conclusion."),
                                         (2, "To support the negative version of the conclusion."),
                                         (3, "To point why a decision on the matter is required soon."),
                                         (4, "To point out missing knowledge on the matter.")))
    choices_heading = ("Pro",
                       "Contra",
                       "Decision required",
                       "Unknowns")

    choices_what = ("The negative version of the following is correct",
                    "The positive version of the following is correct",
                    "The following conclusion needs to be resolved soon",
                    "Humility might be advised upon voting on the following")

    def __init__(self, *args, **kwargs):
        super(Argument,self).__init__(*args, **kwargs)
        self.choice_heading = self.choices_heading[self.aim-1]
        self.choice_what = self.choices_what[self.aim-1]
        self.aim_str = str(self.aim)

    def __str__(self):
        return self.choice_heading + ': ' + str(self.conclusion)

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
