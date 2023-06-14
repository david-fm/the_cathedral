from django import template
from articles.models import BlockImage
register = template.Library()

@register.filter
def index(indexable, i):
    return indexable[i]

@register.filter
def get_comment_from_block(formset, block_id):
    for form in formset:
        if form.block.id == block_id:
            return form
    return None

from django.template.defaulttags import register

@register.filter
def get_value(dictionary, key):
    return dictionary.get(key)