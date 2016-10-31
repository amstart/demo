from django.db import models

from demoslogic.blockobjects.models import BlockObject, VoteBase


class Premise(BlockObject):
    name = 'premise'   #this is used for URL namespaces alongside the class name!
    subject = models.CharField(default = '', max_length = 200)
    predicate = models.CharField(default = '', max_length = 200)
    object = models.CharField(default = '', max_length = 200, blank = True)
    complement = models.CharField(default = '', max_length = 200, blank = True)

    def __init__(self, *args, **kwargs):
        super(Premise,self).__init__(*args, **kwargs)
        self.core_list = [{"textclass":"subject", "value":self.subject},
                          {"textclass":"predicate", "value":self.predicate}]
        if len(self.object) > 0:
            self.core_list.append({"textclass":"object", "value":self.object})
        if len(self.complement ) > 0:
            self.core_list.append({"textclass":"complement", "value":self.complement})

    def __str__(self):
        print_raw = self.subject + " " + self.predicate
        if len(self.object) > 0:
            print_raw = print_raw + " " + self.object
        if len(self.complement ) > 0:
            print_raw = print_raw + " " + self.complement
        return print_raw


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
