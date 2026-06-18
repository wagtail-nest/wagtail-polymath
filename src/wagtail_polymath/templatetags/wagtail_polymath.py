from textwrap import dedent

from django import template
from django.forms.utils import flatatt
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from wagtail_polymath.widgets import MATHJAX_SRI, MATHJAX_VERSION


register = template.Library()


@register.simple_tag
def mathjax_script():
    attributes = {"crossorigin": "anonymous", "integrity": MATHJAX_SRI, "defer": True}
    script = format_html(
        '<script src="{path}"{attributes}></script>',
        path=f"https://cdn.jsdelivr.net/npm/mathjax@{MATHJAX_VERSION}/tex-mml-chtml.js",
        attributes=flatatt(attributes),
    )

    safe_init = mark_safe(  # noqa: S308
        dedent("""
        <script>
            window.MathJax = {
                loader: { load: ["input/asciimath"] },
                tex: { inlineMath: { '[+]': [['$', '$']] } },
            };
        </script>
        """)
    )

    return script + safe_init
