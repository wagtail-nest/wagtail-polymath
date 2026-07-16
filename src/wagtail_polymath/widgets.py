from django import forms
from django.forms import Script
from wagtail.admin.staticfiles import versioned_static

from .settings import get_mathjax_integrity, get_mathjax_url


class MathJaxWidget(forms.Textarea):
    template_name = "wagtail_polymath/mathjaxwidget.html"

    def build_attrs(self, *args, **kwargs):
        attrs = super().build_attrs(*args, **kwargs)
        attrs["data-controller"] = "wagtailmathjax"

        return attrs

    @property
    def media(self):
        attrs = {"defer": True}
        integrity = get_mathjax_integrity()
        if integrity:
            attrs["crossorigin"] = "anonymous"
            attrs["integrity"] = integrity

        return forms.Media(
            js=(
                Script(get_mathjax_url(), **attrs),
                versioned_static("wagtail_polymath/js/wagtail_polymath.js"),
                versioned_static(
                    "wagtail_polymath/js/wagtail_polymath-mathjax-controller.js"
                ),
            )
        )
