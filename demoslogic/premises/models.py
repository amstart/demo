from django.db import models
from django.utils import timezone

from .. models import BlockObject

class Argument(models.Model):
    pass

class Premise(BlockObject):
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


class Vote(BlockObject):
    object = models.ForeignKey(Premise, on_delete = models.CASCADE)
    vote_date = models.DateTimeField('last voted', default = timezone.now)

    class Meta:
        abstract = True


class CategorizationVote(Vote):
    vote_accuracy = models.IntegerField()


#choice has a meta class with the ForeignKey and some API, and the base classes with their specific set of choices
#premises and arguments also might share a meta class
