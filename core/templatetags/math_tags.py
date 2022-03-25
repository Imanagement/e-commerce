from django import template

register = template.Library()


@register.filter
def multiply(value, count):
    return int(value) * int(count)
