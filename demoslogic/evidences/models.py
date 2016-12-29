from django.db import models
from django import forms

from demoslogic.blockobjects.models import NetworkObject, VoteBase
from demoslogic.premises.models import Premise

class Evidence(NetworkObject):
    URL = models.URLField()
    statement = models.ForeignKey(Premise, on_delete = models.CASCADE)
    version = models.IntegerField()
    name_lower = 'evidence'
    name_upper = 'Evidence'
    namespace = 'evidences'   #this is used for URL namespaces!

    def __str__(self):
        return "Evidence for: " + self.statement.get_premise_choice(self.version)

class Vote(VoteBase):
    object = models.ForeignKey(Evidence, on_delete = models.CASCADE)

    class Meta:
        abstract = True

class EvidenceVote(Vote):
    value = models.IntegerField(default = 1,
                                choices = ((0, "neither trustworthy nor relevant"),
                                           (1, "trustworthy, but not relevant"),
                                           (2, "relevant, but not trustworthy"),
                                           (3, "both relevant and trustworthy")))

#choice has a meta class with the ForeignKey and some API, and the base classes with their specific set of choices
#premises and arguments also might share a meta class
