from django import forms
from django.forms import Script
from wagtail.admin.staticfiles import versioned_static

from .settings import wagtail_polymath_settings


class MathJaxWidget(forms.Textarea):
    template_name = "wagtail_polymath/mathjaxwidget.html"

    def build_attrs(self, *args, **kwargs):
        attrs = super().build_attrs(*args, **kwargs)
        attrs["data-controller"] = "wagtailmathjax"

        return attrs

    @property
    def media(self):
        attrs = {"defer": True}
        integrity = wagtail_polymath_settings.mathjax_sri
        if integrity:
            attrs["crossorigin"] = "anonymous"
            attrs["integrity"] = integrity

        return forms.Media(
            js=(
                Script(wagtail_polymath_settings.mathjax_url, **attrs),
                versioned_static("wagtail_polymath/js/wagtail_polymath.js"),
                versioned_static(
                    "wagtail_polymath/js/wagtail_polymath-mathjax-controller.js"
                ),
            )
        )
