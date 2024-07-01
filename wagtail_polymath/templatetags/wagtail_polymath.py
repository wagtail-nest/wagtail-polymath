from django import template
from django.utils.html import format_html, format_html_join

from wagtail_polymath.config import get_polymath_config


register = template.Library()


@register.simple_tag
def polymath_js():
    return format_html_join(
        "\n",
        "{0}",
        [
            (
                format_html(
                    '<script src="{}"></script>',
                    js,
                ),
            )
            for js in get_polymath_config("js")
        ],
    )
