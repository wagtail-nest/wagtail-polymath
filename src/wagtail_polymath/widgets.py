from django import forms
from django.forms import Script
from wagtail.admin.staticfiles import versioned_static


MATHJAX_VERSION = "4.1.2"
MATHJAX_SRI = "sha256-dPV35kaoLq1rg+JbYf8p1kTrZamwMY+XIwaWUPwqtpU="


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
                    f"https://cdn.jsdelivr.net/npm/mathjax@{MATHJAX_VERSION}/tex-mml-chtml.js",
                    **{
                        "crossorigin": "anonymous",
                        "integrity": MATHJAX_SRI,
                        "defer": True,
                    },
                ),
                versioned_static("wagtail_polymath/js/wagtail_polymath.js"),
                versioned_static(
                    "wagtail_polymath/js/wagtail_polymath-mathjax-controller.js"
                ),
            )
        )
