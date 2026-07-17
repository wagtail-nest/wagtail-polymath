from django import template
from django.forms.utils import flatatt
from django.utils.html import format_html
from wagtail.admin.staticfiles import versioned_static

from wagtail_polymath.settings import wagtail_polymath_settings


register = template.Library()


@register.simple_tag
def mathjax_script():
    attributes = {"defer": True}
    integrity = wagtail_polymath_settings.mathjax_sri
    if integrity:
        attributes["crossorigin"] = "anonymous"
        attributes["integrity"] = integrity

    return format_html(
        '<script src="{init_path}"></script><script src="{path}"{attributes}></script>',
        init_path=versioned_static("wagtail_polymath/js/mathjax_init.js"),
        path=wagtail_polymath_settings.mathjax_url,
        attributes=flatatt(attributes),
    )
