from django import template
register = template.Library()

@register.filter
def index(indexable, i):
    return indexable[i]

from django.template.defaulttags import register

@register.filter
def get_value(dictionary, key):
    return dictionary.get(key)