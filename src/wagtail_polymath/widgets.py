from django import forms
from wagtail import VERSION as WAGTAIL_VERSION

from wagtail_polymath.config import get_polymath_config


class MathJaxWidgetBase(forms.Textarea):
    template_name = "wagtail_polymath/mathjaxwidget.html"

    def _get_media_js(self):
        return get_polymath_config("js")

    def _get_media_css(self):
        return {"all": get_polymath_config("css")}

    @property
    def media(self):
        return forms.Media(js=self._get_media_js(), css=self._get_media_css())


if WAGTAIL_VERSION >= (6, 0):

    class MathJaxWidget(MathJaxWidgetBase):
        def build_attrs(self, *args, **kwargs):
            attrs = super().build_attrs(*args, **kwargs)
            attrs["data-controller"] = "wagtailmathjax"

            return attrs

        def _get_media_js(self):
            return super()._get_media_js() + get_polymath_config("widget")

else:
    from wagtail.telepath import register
    from wagtail.utils.widgets import WidgetWithScript
    from wagtail.widget_adapters import WidgetAdapter

    class MathJaxWidget(WidgetWithScript, MathJaxWidgetBase):
        def render_js_init(self, id_, name, value):
            return f'initMathJaxPreview("{id_}");'

    class MathJaxAdapter(WidgetAdapter):
        js_constructor = "wagtail_polymath.widgets.MathJaxWidget"

        class Media:
            # TODO: remove the adapter when dropping support for Wagtail 5.2
            js = get_polymath_config("widget")

    register(MathJaxAdapter(), MathJaxWidget)
