from typing import NotRequired, Required, TypedDict

from django.conf import settings


class LibraryDict(TypedDict):
    url: Required[str]
    sri: NotRequired[str | None]


class EngineDict(TypedDict):
    libraries: Required[list[LibraryDict]]
    widget_js: NotRequired[list[str]]


MATHJAX_VERSION = "4.1.2"
KATEX_VERSION = "0.18.7"

ENGINES: dict[str, EngineDict] = {
    "mathjax": {
        "libraries": [
            {
                "url": f"https://cdn.jsdelivr.net/npm/mathjax@{MATHJAX_VERSION}/tex-mml-chtml.js",
                "sri": "sha256-dPV35kaoLq1rg+JbYf8p1kTrZamwMY+XIwaWUPwqtpU=",
            },
        ],
        "widget_js": [
            "wagtail_polymath/js/wagtail_polymath-mathjax-widget.js",
            "wagtail_polymath/js/wagtail_polymath-preview-controller.js",
        ],
    },
    "katex": {
        "libraries": [
            {
                "url": f"https://cdn.jsdelivr.net/npm/katex@{KATEX_VERSION}/dist/katex.min.js",
                "sri": "sha384-+7Keh381hSkXmXqnjC0JBM/kzsN6TFj+wMKychSLjTvJ8/0ElMde2uKl8i6p6Buj",
            },
            {
                "url": f"https://cdn.jsdelivr.net/npm/katex@{KATEX_VERSION}/dist/contrib/auto-render.min.js",
                "sri": "sha384-bjyGPfbij8/NDKJhSGZNP/khQVgtHUE5exjm4Ydllo42FwIgYsdLO2lXGmRBf5Mz",
            },
            {
                "url": f"https://cdn.jsdelivr.net/npm/katex@{KATEX_VERSION}/dist/katex.min.css",
                "sri": "sha384-JctiRyLzXCrSoOOzFlSoWLdyzQl7OrrRnhyeBmzB6ZWtcjccUyc8lCQJqIbs3uQX",
            },
        ],
        "widget_js": [
            "wagtail_polymath/js/wagtail_polymath-katex-widget.js",
            "wagtail_polymath/js/wagtail_polymath-preview-controller.js",
        ],
    },
}


class WagtailPolymathSettings:
    """
    Shadows Django's settings, exposing the WAGTAIL_POLYMATH dict as attributes.
    For example:
        from wagtail_polymath.settings import wagtail_polymath_settings
        print(wagtail_polymath_settings.library_url)
    """

    @property
    def _user_settings(self) -> dict[str, EngineDict]:
        user_settings = getattr(settings, "WAGTAIL_POLYMATH", None)
        return user_settings if isinstance(user_settings, dict) else {}

    @property
    def engine(self) -> str:
        user_engine = self._user_settings.get("engine")
        if user_engine and user_engine in ENGINES:
            return user_engine
        return "mathjax"

    @property
    def libraries(self) -> list[LibraryDict]:
        return self._user_settings.get("libraries") or ENGINES[self.engine]["libraries"]

    @property
    def widget_media_js(self) -> list[str]:
        return ENGINES[self.engine].get("widget_js", [])


wagtail_polymath_settings = WagtailPolymathSettings()
