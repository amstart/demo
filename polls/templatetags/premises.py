from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def premise_print_with_class(premise):
    string_with_class = ""
    for element in premise.core_list:
        string_with_class = string_with_class + "<span class=\"" + element["textclass"] + "\">" + \
        conditional_escape(element["value"]) + "</span> "
    return mark_safe(string_with_class)
