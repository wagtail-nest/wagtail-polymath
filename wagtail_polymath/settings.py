from django.conf import settings


DEFAULT_ENGINE = "mathjax"

DEFAULT_MATHJAX_SETTINGS = {
    "js": [
        "https://cdn.jsdelivr.net/npm/mathjax@2/MathJax.js?config=TeX-MML-AM_CHTML",
    ],
    "config": "wagtail_polymath/js/mathjax_config.js",
}

DEFAULT_KATEX_SETTINGS = {
    "css": ["https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.css"],
    "js": [
        "https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.js",
        "https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/contrib/auto-render.min.js",
    ],
}

WAGTAILPOLYMATH_ENGINE = getattr(settings, "WAGTAILPOLYMATH_ENGINE", DEFAULT_ENGINE)
WAGTAILPOLYMATH_SETTINGS = getattr(
    settings,
    "WAGTAILPOLYMATH_SETTINGS",
    globals()[f"DEFAULT_{WAGTAILPOLYMATH_ENGINE.upper()}_SETTINGS"],
)
