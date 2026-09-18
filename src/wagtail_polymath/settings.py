from typing import NotRequired, Required, TypedDict

from django.conf import settings


class EngineDict(TypedDict):
    library_url: Required[str]
    sri: NotRequired[str]
    js: NotRequired[list[str]]
    css: NotRequired[list[str]]


MATHJAX_VERSION = "4.1.2"

ENGINES: dict[str, EngineDict] = {
    "mathjax": {
        "library_url": f"https://cdn.jsdelivr.net/npm/mathjax@{MATHJAX_VERSION}/tex-mml-chtml.js",
        "sri": "sha256-dPV35kaoLq1rg+JbYf8p1kTrZamwMY+XIwaWUPwqtpU=",
        "js": [
            "wagtail_polymath/js/wagtail_polymath-mathjax-widget.js",
            "wagtail_polymath/js/wagtail_polymath-mathjax-controller.js",
        ],
    }
}


class WagtailPolymathSettings:
    """
    Shadows Django's settings, exposing the WAGTAIL_POLYMATH dict as attributes.
    For example:
        from wagtail_polymath.settings import wagtail_polymath_settings
        print(wagtail_polymath_settings.library_url)
    """

    @property
    def _user_settings(self) -> dict[str, str]:
        user_settings = getattr(settings, "WAGTAIL_POLYMATH", None)
        return user_settings if isinstance(user_settings, dict) else {}

    @property
    def engine(self) -> str:
        user_engine = self._user_settings.get("engine")
        if user_engine and user_engine in ENGINES:
            return user_engine
        return "mathjax"

    @property
    def library_url(self) -> str:
        return (
            self._user_settings.get("library_url")
            or ENGINES[self.engine]["library_url"]
        )

    @property
    def library_sri(self) -> str | None:
        if self._user_settings.get("library_url"):
            # We can't know the hash for a script we don't control, so a
            # custom URL without a matching library_url setting intentionally
            # omits integrity checking rather than erroring.
            return self._user_settings.get("library_sri")
        return ENGINES[self.engine]["library_url"]

    @property
    def widget_media_js(self) -> list[str]:
        return ENGINES[self.engine].get("js", [])


wagtail_polymath_settings = WagtailPolymathSettings()
