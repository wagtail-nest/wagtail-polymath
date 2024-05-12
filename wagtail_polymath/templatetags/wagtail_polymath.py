from django import template
from django.templatetags.static import static
from django.utils.html import format_html, format_html_join

from ..settings import WAGTAILPOLYMATH_ENGINE
from ..wagtail_hooks import polymath_config_js, polymath_css, polymath_js


register = template.Library()


@register.simple_tag
def wagtail_polymath_css():
    return polymath_css()


@register.simple_tag
def wagtail_polymath_js():
    js = [(polymath_js(),), (polymath_config_js(),)]
    if WAGTAILPOLYMATH_ENGINE == "katex":
        js.append(
            (
                format_html(
                    '<script src="{}"></script>',
                    static("wagtail_polymath/js/katex_render_body.js"),
                ),
            )
        )

    return format_html_join("\n", "{0}", js)
