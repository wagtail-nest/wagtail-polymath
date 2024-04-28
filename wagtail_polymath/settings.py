from django.conf import settings


DEFAULT_SETTINGS = {
    "js": "https://cdn.jsdelivr.net/npm/mathjax@2/MathJax.js?config=TeX-MML-AM_CHTML",
}

WAGTAILPOLYMATH_SETTINGS = getattr(
    settings, "WAGTAILPOLYMATH_SETTINGS", DEFAULT_SETTINGS
)
