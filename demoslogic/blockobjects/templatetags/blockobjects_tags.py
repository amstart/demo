import json

from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.utils.safestring import mark_safe
from django.template import Library
from django.utils.html import conditional_escape

from demoslogic.premises.models import Premise

register = Library()

def jsonify(object):
    if isinstance(object, QuerySet):
        return mark_safe(serialize('json', object))
    return mark_safe(json.dumps(object))

register.filter('jsonify', jsonify)
jsonify.is_safe = True

def print_premise(object):
    string_with_class = ""
    for element in object.core_list:
        string_with_class = string_with_class + \
                            "<span class=\"" + \
                            element["textclass"] + "\">" + \
                            conditional_escape(element["value"]) + "</span> "
    return mark_safe(string_with_class)

@register.simple_tag
def print_with_class(object):
    if type(object) == Premise:
        return print_premise(object)
    else:
        text = conditional_escape(object.choice_headings[object.aim-1])
        string_with_class = "<span class=\"aim-" + \
                            str(object.aim) + "\">" + \
                            text + ":</span> "  + \
                            print_premise(object.conclusion)
        return mark_safe(string_with_class)
