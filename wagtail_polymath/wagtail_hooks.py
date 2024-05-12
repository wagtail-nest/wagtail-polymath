from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.templatetags.static import static
from django.utils.html import format_html, format_html_join
from wagtail import hooks

from wagtail_polymath.settings import WAGTAILPOLYMATH_SETTINGS


def url(path):
    validate = URLValidator()
    try:
        validate(path)
        return path
    except ValidationError:
        return static(path)


@hooks.register("insert_global_admin_css")
def polymath_css():
    if WAGTAILPOLYMATH_SETTINGS.get("css", None):
        return format_html_join(
            "\n",
            '<link rel="stylesheet" href="{0}"></script>',
            ((url(path),) for path in WAGTAILPOLYMATH_SETTINGS["css"]),
        )
    else:
        return ""


@hooks.register("insert_editor_js")
def polymath_js():
    if WAGTAILPOLYMATH_SETTINGS.get("js", None):
        return format_html_join(
            "\n",
            '<script src="{0}"></script>',
            ((url(path),) for path in WAGTAILPOLYMATH_SETTINGS["js"]),
        )
    else:
        return ""


@hooks.register("insert_editor_js")
def polymath_config_js():
    if WAGTAILPOLYMATH_SETTINGS.get("config", None):
        return format_html(
            '<script src="{}"></script>',
            url(WAGTAILPOLYMATH_SETTINGS["config"]),
        )
    else:
        return ""
