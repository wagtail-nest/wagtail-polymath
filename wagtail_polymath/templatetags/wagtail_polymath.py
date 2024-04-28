from django import template

from wagtail_polymath.settings import WAGTAILPOLYMATH_SETTINGS


register = template.Library()


@register.simple_tag
def mathjax():
    return WAGTAILPOLYMATH_SETTINGS["js"]
