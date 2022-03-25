from django import template

register = template.Library()

@register.filter
def calculate_summary_in_credit(summary, credit_duration=24, *args, **kwargs):
    """ Calculating credit sum for one or more products."""
    r = 0.01
    n = credit_duration
    pv = summary
    com_percent = 0.0155
    com_mdl = 0
    if n == 6:
        com_percent = 0.0125
        com_mdl = 25
    if n == 24:
        com_mdl = 25
    result = (((r * pv) / (1 - (1 + r) ** (-n))) + pv * com_percent + com_mdl)
    return round(result)
