from typing import TYPE_CHECKING, Any

from django.forms import Media, Script, Textarea
from wagtail.admin.staticfiles import versioned_static

from .compat import Stylesheet
from .config import wagtail_polymath_config


if TYPE_CHECKING:
    from .config import LibraryDict

__all__ = ["PolymathTextareaWidget"]


class PolymathTextareaWidget(Textarea):
    template_name = "wagtail_polymath/polymath-textarea-widget.html"

    def build_attrs(
        self, base_attrs: dict[str, Any], extra_attrs: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        attrs = super().build_attrs(base_attrs, **(extra_attrs or {}))
        attrs["data-controller"] = "polymath-textarea-controller"

        return attrs

    def _media_attrs(
        self, library: "LibraryDict", defer: bool = True
    ) -> dict[str, str | bool]:
        attrs = {}
        if defer:
            attrs["defer"] = True

        if sri := library.get("sri", "").strip():
            attrs["crossorigin"] = "anonymous"
            attrs["integrity"] = sri

        return attrs

    @property
    def media(self) -> Media:
        scripts = []
        stylesheets = []
        for library in wagtail_polymath_config.libraries_js:
            scripts.append(Script(library["url"], **self._media_attrs(library)))

        for library in wagtail_polymath_config.libraries_css:
            stylesheets.append(
                Stylesheet(
                    library["url"],
                    media="all",
                    **self._media_attrs(library, defer=False),
                )
            )

        js = [
            *scripts,
            *[
                versioned_static(script)
                for script in wagtail_polymath_config.widget_media_js
            ],
        ]

        return Media(js=js, css={"all": stylesheets} if stylesheets else None)
