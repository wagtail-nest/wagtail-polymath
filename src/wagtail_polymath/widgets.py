from django import forms
from django.forms import Script
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
        attrs = {"defer": True}
        integrity = wagtail_polymath_settings.library_sri
        if integrity:
            attrs["crossorigin"] = "anonymous"
            attrs["integrity"] = integrity

        js = [
            Script(wagtail_polymath_settings.library_url, **attrs),
            *[
                versioned_static(script)
                for script in wagtail_polymath_settings.widget_media_js
            ],
            versioned_static(
                "wagtail_polymath/js/wagtail_polymath-preview-controller.js"
            ),
        ]

        return forms.Media(js=js)
