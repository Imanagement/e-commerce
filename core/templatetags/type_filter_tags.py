from django import template

register = template.Library()


@register.filter
def value_is_int(value):
    return True if type(value) is int else False


@register.filter
def to_int(value):
    try:
        result = int(value)
        return result
    except Exception:
        return None
