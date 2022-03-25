from django import template

register = template.Library()


@register.filter
def get(dict, key):
    return dict.get(key) or ''


@register.filter
def get_value(dict, key):
    return dict.get(key).values() or ""


@register.simple_tag
def minus(number1, number2):
    try:
        if isinstance(number1, int) and isinstance(number2, int):
            return number1 - number2
        else:
            return 0
    except Exception:
        return 0
