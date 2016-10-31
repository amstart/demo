from django.db import models

from demoslogic.blockobjects.models import BlockObject, VoteBase

class Argument(BlockObject):
    name = 'argument'   #this is used for URL namespaces alongside the class name!
    aim = models.IntegerField(default = 1,
                              choices = ((1, "To support the positive version of the conclusion."),
                                         (2, "To support the negative version of the conclusion."),
                                         (3, "To point why the conclusion should be resolved soon, if possible."),
                                         (4, "To point out missing knowledge on the matter.")))

class Vote(VoteBase):
    object = models.ForeignKey(Argument, on_delete = models.CASCADE)

    class Meta:
        abstract = True
