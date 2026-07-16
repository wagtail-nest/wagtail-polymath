from django.conf import settings


MATHJAX_VERSION = "4.1.2"
MATHJAX_DEFAULT_URL = (
    f"https://cdn.jsdelivr.net/npm/mathjax@{MATHJAX_VERSION}/tex-mml-chtml.js"
)
MATHJAX_DEFAULT_SRI = "sha256-dPV35kaoLq1rg+JbYf8p1kTrZamwMY+XIwaWUPwqtpU="


def get_mathjax_url():
    return getattr(settings, "WAGTAILPOLYMATH_MATHJAX_URL", None) or MATHJAX_DEFAULT_URL


def get_mathjax_integrity():
    if getattr(settings, "WAGTAILPOLYMATH_MATHJAX_URL", None):
        return getattr(settings, "WAGTAILPOLYMATH_MATHJAX_SRI", None)
    return MATHJAX_DEFAULT_SRI
