from django import template
from core.utils import encode_id

register = template.Library()

@register.filter
def encodeid(value):
    """Перетворює числовий id в hashid"""
    return encode_id(value)