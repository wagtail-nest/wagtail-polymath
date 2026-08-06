from django import forms
from wagtail.admin.staticfiles import versioned_static

from .settings import wagtail_polymath_settings


class MathJaxWidget(forms.Textarea):
    template_name = "wagtailmath/mathjaxwidget.html"

    def build_attrs(self, *args, **kwargs):
        attrs = super().build_attrs(*args, **kwargs)
        attrs["data-controller"] = "wagtailmathjax"

        return attrs

    @property
    def media(self):
        # PORT NOTE: 2.x also passes defer=True here. We can't: wagtailmath.js
        # and the Stimulus controller are not deferred, and
        # initMathJaxPreview() calls MathJax.Callback() as soon as it runs, so
        # deferring only the CDN script would leave MathJax undefined at that
        # point and break the live preview.
        attributes = {}
        if integrity := wagtail_polymath_settings.mathjax_sri:
            attributes["crossorigin"] = "anonymous"
            attributes["integrity"] = integrity

        return forms.Media(
            js=(
                forms.Script(wagtail_polymath_settings.mathjax_url, **attributes),
                versioned_static("wagtailmath/js/wagtailmath.js"),
                versioned_static("wagtailmath/js/wagtailmath-mathjax-controller.js"),
            )
        )
