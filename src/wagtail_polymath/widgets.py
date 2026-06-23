from django import forms
from django.forms import Script
from wagtail.admin.staticfiles import versioned_static


class MathJaxWidget(forms.Textarea):
    template_name = "wagtail_polymath/mathjaxwidget.html"

    def build_attrs(self, *args, **kwargs):
        attrs = super().build_attrs(*args, **kwargs)
        attrs["data-controller"] = "wagtailmathjax"

        return attrs

    @property
    def media(self):
        return forms.Media(
            js=(
                Script(
                    versioned_static(
                        "wagtail_polymath/js/vendor/mathjax/tex-mml-chtml.js"
                    ),
                    defer=True,
                ),
                versioned_static("wagtail_polymath/js/wagtail_polymath.js"),
                versioned_static(
                    "wagtail_polymath/js/wagtail_polymath-mathjax-controller.js"
                ),
            )
        )
