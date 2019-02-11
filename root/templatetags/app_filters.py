from django import template

register = template.Library()


@register.filter(name='as_percentage')
def as_percentage(value):
    return value * 100
