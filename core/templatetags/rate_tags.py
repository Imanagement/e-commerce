from django import template
from core.models import Basket

register = template.Library()


@register.simple_tag
def calculate_reviews_percents(review_count, total_reviews_count):
    one_percent = total_reviews_count / 100
    return review_count / one_percent


@register.filter
def get(dict, key):
    return dict.get(key) or ''
