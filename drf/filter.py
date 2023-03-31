import datetime
from django import template

register = template.Library()


@register.filter
def multiply(value, arg):
    return value * arg

#register.filter('my_filter_name', my_filter_name)