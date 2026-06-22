from django import template
from django.forms.utils import flatatt
from django.utils.html import format_html
from wagtail.admin.staticfiles import versioned_static

from wagtail_polymath.widgets import MATHJAX_SRI, MATHJAX_VERSION


register = template.Library()


@register.simple_tag
def mathjax_script():
    attributes = {"crossorigin": "anonymous", "integrity": MATHJAX_SRI, "defer": True}
    return format_html(
        '<script src="{init_path}"></script><script src="{path}"{attributes}></script>',
        init_path=versioned_static("wagtail_polymath/js/mathjax_init.js"),
        path=f"https://cdn.jsdelivr.net/npm/mathjax@{MATHJAX_VERSION}/tex-mml-chtml.js",
        attributes=flatatt(attributes),
    )
