from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.exceptions import ImproperlyConfigured
from wagtail import VERSION as WAGTAIL_VERSION
from wagtail.admin.staticfiles import versioned_static


# The path could be static files or external URLs.
DEFAULT_MATHJAX_SETTINGS = {
    "js": [
        "https://cdn.jsdelivr.net/npm/mathjax@2/MathJax.js?config=TeX-MML-AM_CHTML",
    ],
    "widget": [
        "wagtail_polymath/js/polymath-widget-mathjax.js",
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

polymath_settings = getattr(settings, "WAGTAIL_POLYMATH", "mathjax")
if isinstance(polymath_settings, str):
    if polymath_settings == "mathjax":
        POLYMATH_SETTINGS = DEFAULT_MATHJAX_SETTINGS
    elif polymath_settings == "katex":
        POLYMATH_SETTINGS = DEFAULT_KATEX_SETTINGS
    else:
        raise ImproperlyConfigured(
            f"WAGTAIL_POLYMATH: invalid typesetting engine: `{polymath_settings}` (valid options: 'mathjax', 'katex')"
        )
elif isinstance(polymath_settings, dict):
    POLYMATH_SETTINGS = polymath_settings
else:
    raise ImproperlyConfigured("WAGTAIL_POLYMATH: invalid settings")

if WAGTAIL_VERSION >= (6, 0):
    POLYMATH_SETTINGS["widget"].append(
        "wagtail_polymath/js/polymath-textarea-controller.js",
    )
else:
    POLYMATH_SETTINGS["widget"].append(
        "wagtail_polymath/js/polymath-textarea-adapter.js",
    )


def get_polymath_config(key):
    paths = POLYMATH_SETTINGS.get(key, [])

    # Return absolute path to the asset if it's a static file path.
    return [versioned_static(path) if finders.find(path) else path for path in paths]
