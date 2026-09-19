from typing import TYPE_CHECKING

from django import forms
from django.forms import Script, Stylesheet
from wagtail.admin.staticfiles import versioned_static

from .settings import wagtail_polymath_settings


if TYPE_CHECKING:
    from .settings import LibraryDict

__all__ = ["PolymathTextareaWidget"]


class PolymathTextareaWidget(forms.Textarea):
    template_name = "wagtail_polymath/polymath-textarea-widget.html"

    def build_attrs(self, *args, **kwargs):
        attrs = super().build_attrs(*args, **kwargs)
        attrs["data-controller"] = "polymath-textarea-controller"

        return attrs

    def _media_attrs(
        self, library: "LibraryDict", defer: bool = True
    ) -> dict[str, str | bool]:
        attrs = {}
        if defer:
            attrs["defer"] = True

        if sri := library["sri"].strip():
            attrs["crossorigin"] = "anonymous"
            attrs["integrity"] = sri

        return attrs

    @property
    def media(self):
        scripts = []
        stylesheets = []
        for library in wagtail_polymath_settings.libraries_js:
            scripts.append(Script(library["url"], **self._media_attrs(library)))

        for library in wagtail_polymath_settings.libraries_css:
            stylesheets.append(
                Stylesheet(library["url"], **self._media_attrs(library, defer=False))
            )

        js = [
            *scripts,
            *[
                versioned_static(script)
                for script in wagtail_polymath_settings.widget_media_js
            ],
        ]

        return forms.Media(js=js, css={"all": stylesheets} if stylesheets else None)
