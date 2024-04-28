from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.templatetags.static import static
from django.utils.html import format_html
from wagtail import hooks

from wagtail_polymath.settings import WAGTAILPOLYMATH_SETTINGS


@hooks.register("insert_global_admin_js")
def global_mathjax_js():
    validate = URLValidator()
    try:
        validate(WAGTAILPOLYMATH_SETTINGS["js"])
        url = WAGTAILPOLYMATH_SETTINGS["js"]
    except ValidationError:
        url = static(WAGTAILPOLYMATH_SETTINGS["js"])

    return format_html('<script src="{}"></script>', url)
