from django import forms
from wagtail.admin.staticfiles import versioned_static


MATHJAX_VERSION = "2.7.9"


class MathJaxWidget(forms.Textarea):
    template_name = "wagtailmath/mathjaxwidget.html"

    def build_attrs(self, *args, **kwargs):
        attrs = super().build_attrs(*args, **kwargs)
        attrs["data-controller"] = "wagtailmathjax"

        return attrs

    @property
    def media(self):
        return forms.Media(
            js=(
                f"https://cdnjs.cloudflare.com/ajax/libs/mathjax/{MATHJAX_VERSION}/MathJax.js?config=TeX-MML-AM_HTMLorMML",
                versioned_static("wagtailmath/js/wagtailmath.js"),
                versioned_static("wagtailmath/js/wagtailmath-mathjax-controller.js"),
            )
        )
