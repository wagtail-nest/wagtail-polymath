from django.conf import settings


MATHJAX_VERSION = "2.7.9"
# PORT NOTE: 2.x defaults to MathJax 4.1.2 on jsdelivr, whose entry point is a
# bare `tex-mml-chtml.js`. MathJax 2 loads no input/output processors without a
# combined config in the URL, so the default carries the `?config=` that
# widgets.py used to hardcode. TeX-MML-AM_HTMLorMML is the value the admin
# widget has always used.
MATHJAX_DEFAULT_URL = f"https://cdnjs.cloudflare.com/ajax/libs/mathjax/{MATHJAX_VERSION}/MathJax.js?config=TeX-MML-AM_HTMLorMML"
# PORT NOTE: hash published by cdnjs for this file. Unlike 2.x, which already
# shipped an SRI hash before the change being backported, 1.3.1 and earlier
# loaded MathJax with no integrity checking at all, so this is new on 1.x.
MATHJAX_DEFAULT_SRI = "sha512-M36RUChWzAh1veeenRZFql7HydLEnkYmoloiCvVrhz402UZgKI93qkV7SsaxtVKdN95Wzajh39ysrXCq34NTsg=="


class WagtailPolymathSettings:
    """
    Shadows Django's settings, exposing the WAGTAIL_POLYMATH dict as attributes.
    For example:
        from wagtailmath.settings import wagtail_polymath_settings
        print(wagtail_polymath_settings.mathjax_url)
    """

    # PORT NOTE: the dict is deliberately called WAGTAIL_POLYMATH, matching 2.x,
    # even though the module here is still `wagtailmath`. Anyone who configures
    # a custom CDN on 1.4.0 then needs no settings change when they upgrade.

    @property
    def _user_settings(self):
        user_settings = getattr(settings, "WAGTAIL_POLYMATH", None)
        return user_settings if isinstance(user_settings, dict) else {}

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
