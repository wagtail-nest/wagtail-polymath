from django import forms
from wagtail import VERSION as WAGTAIL_VERSION
from wagtail.admin.staticfiles import versioned_static


MATHJAX_VERSION = "2.7.9"


class MathJaxWidgetBase(forms.Textarea):
    template_name = "wagtailmath/mathjaxwidget.html"

    def _get_media_js(self):
        return (
            f"https://cdnjs.cloudflare.com/ajax/libs/mathjax/{MATHJAX_VERSION}/MathJax.js?config=TeX-MML-AM_HTMLorMML",
            versioned_static("wagtailmath/js/wagtailmath.js"),
        )

    @property
    def media(self):
        return forms.Media(js=self._get_media_js())


if WAGTAIL_VERSION >= (6, 0):

    class MathJaxWidget(MathJaxWidgetBase):
        def build_attrs(self, *args, **kwargs):
            attrs = super().build_attrs(*args, **kwargs)
            attrs["data-controller"] = "wagtailmathjax"

            return attrs

        def _get_media_js(self):
            return (
                *super()._get_media_js(),
                versioned_static("wagtailmath/js/wagtailmath-mathjax-controller.js"),
            )
else:
    from wagtail.telepath import register
    from wagtail.utils.widgets import WidgetWithScript
    from wagtail.widget_adapters import WidgetAdapter

    class MathJaxWidget(WidgetWithScript, MathJaxWidgetBase):
        def render_js_init(self, id_, name, value):
            return f'initMathJaxPreview("{id_}");'

    class MathJaxAdapter(WidgetAdapter):
        js_constructor = "wagtailmath.widgets.MathJaxWidget"

        class Media:
            # TODO: remove the adapter when dropping support for Wagtail 5.2
            js = ["wagtailmath/js/mathjax-textarea-adapter.js"]

    register(MathJaxAdapter(), MathJaxWidget)
