from django.conf import settings
from django.contrib.staticfiles import finders
from wagtail import VERSION as WAGTAIL_VERSION
from wagtail.admin.staticfiles import versioned_static


# The path could be static files or external URLs.
DEFAULT_SETTINGS = {
    "js": [
        "https://cdn.jsdelivr.net/npm/mathjax@2/MathJax.js?config=TeX-MML-AM_CHTML",
    ],
    "widget": [
        "wagtail_polymath/js/wagtailmath.js",
    ],
}

if WAGTAIL_VERSION >= (6, 0):
    DEFAULT_SETTINGS["widget"].append(
        "wagtail_polymath/js/wagtailmath-mathjax-controller.js",
    )
else:
    DEFAULT_SETTINGS["widget"].append(
        "wagtail_polymath/js/mathjax-textarea-adapter.js",
    )

WAGTAILPOLYMATH_SETTINGS = DEFAULT_SETTINGS
WAGTAILPOLYMATH_SETTINGS.update(getattr(settings, "WAGTAILPOLYMATH_SETTINGS", {}))


def get_polymath_config(key):
    paths = WAGTAILPOLYMATH_SETTINGS.get(key, [])

    # Return absolute path to the asset if it's a static file path.
    return [versioned_static(path) if finders.find(path) else path for path in paths]
