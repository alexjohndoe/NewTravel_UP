# main/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter(name='split')
def split(value, delimiter=','):
    return [item.strip() for item in value.split(delimiter)]