from urllib.parse import urlparse

from django import forms
from django.forms import Script, Stylesheet
from wagtail.admin.staticfiles import versioned_static

from .settings import wagtail_polymath_settings


__all__ = ["PolymathTextareaWidget"]


class PolymathTextareaWidget(forms.Textarea):
    template_name = "wagtail_polymath/polymath-textarea-widget.html"

    def build_attrs(self, *args, **kwargs):
        attrs = super().build_attrs(*args, **kwargs)
        attrs["data-controller"] = "polymath-textarea-controller"

        return attrs

    @property
    def media(self):
        scripts = []
        stylesheets = []
        for library in wagtail_polymath_settings.libraries:
            attrs = {"defer": True}
            if sri := library["sri"].strip():
                attrs["crossorigin"] = "anonymous"
                attrs["integrity"] = sri

            url = library["url"].strip()
            if urlparse(url).path.endswith(".css"):
                stylesheets.append(Stylesheet(url, **attrs))
            else:
                scripts.append(Script(url, **attrs))

        js = [
            *scripts,
            *[
                versioned_static(script)
                for script in wagtail_polymath_settings.widget_media_js
            ],
        ]

        return forms.Media(js=js, css={"all": stylesheets} if stylesheets else None)
