from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.exceptions import ImproperlyConfigured
from wagtail import VERSION as WAGTAIL_VERSION
from wagtail.admin.staticfiles import versioned_static


TYPESETTING_ENGINE = getattr(settings, "WAGTAILPOLYMATH_ENGINE", "mathjax")

# The path could be static files or external URLs.
DEFAULT_MATHJAX_SETTINGS = {
    "js": [
        "https://cdn.jsdelivr.net/npm/mathjax@2/MathJax.js?config=TeX-MML-AM_CHTML",
    ],
    "widget": [
        "wagtail_polymath/js/wagtailmath.js",
    ],
}

DEFAULT_KATEX_SETTINGS = {
    "js": [
        "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js",
        "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js",
    ],
    "widget": [
        "wagtail_polymath/js/polymath-widget-katex.js",
    ],
    "css": ["https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css"],
}

if TYPESETTING_ENGINE == "mathjax":
    DEFAULT_SETTINGS = DEFAULT_MATHJAX_SETTINGS
elif TYPESETTING_ENGINE == "katex":
    DEFAULT_SETTINGS = DEFAULT_KATEX_SETTINGS
else:
    raise ImproperlyConfigured(
        f"WAGTAILPOLYMATH_ENGINE: invalid typesetting engine: `{TYPESETTING_ENGINE}` "
        "(valid options: 'mathjax', 'katex')"
    )

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
