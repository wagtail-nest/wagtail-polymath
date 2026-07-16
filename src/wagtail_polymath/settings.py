from django.conf import settings


MATHJAX_VERSION = "4.1.2"
MATHJAX_DEFAULT_URL = (
    f"https://cdn.jsdelivr.net/npm/mathjax@{MATHJAX_VERSION}/tex-mml-chtml.js"
)
MATHJAX_DEFAULT_SRI = "sha256-dPV35kaoLq1rg+JbYf8p1kTrZamwMY+XIwaWUPwqtpU="


class WagtailPolymathSettings:
    """
    Shadows Django's settings, exposing the WAGTAIL_POLYMATH dict as attributes.
    For example:
        from wagtail_polymath.settings import wagtail_polymath_settings
        print(wagtail_polymath_settings.mathjax_url)
    """

    @property
    def _user_settings(self):
        return getattr(settings, "WAGTAIL_POLYMATH", {})

    @property
    def mathjax_url(self):
        return self._user_settings.get("mathjax_url") or MATHJAX_DEFAULT_URL

    @property
    def mathjax_sri(self):
        if self._user_settings.get("mathjax_url"):
            # We can't know the hash for a script we don't control, so a
            # custom URL without a matching mathjax_sri setting intentionally
            # omits integrity checking rather than erroring.
            return self._user_settings.get("mathjax_sri")
        return MATHJAX_DEFAULT_SRI


wagtail_polymath_settings = WagtailPolymathSettings()
