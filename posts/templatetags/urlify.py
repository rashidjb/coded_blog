from django import template
from urllib.parse import quote

register = template.Library()

@register.filter
def urlify(plainText):
	return quote(plainText)