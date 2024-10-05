from django import forms
from wagtail import VERSION as WAGTAIL_VERSION

from wagtail_polymath.config import get_polymath_config


class PolymathTextareaWidgetBase(forms.Textarea):
    template_name = "wagtail_polymath/textarea-widget.html"

    def _get_media_js(self):
        return get_polymath_config("js")

    def _get_media_css(self):
        return {"all": get_polymath_config("css")}

    @property
    def media(self):
        return forms.Media(js=self._get_media_js(), css=self._get_media_css())


if WAGTAIL_VERSION >= (6, 0):

    class PolymathTextareaWidget(PolymathTextareaWidgetBase):
        def build_attrs(self, *args, **kwargs):
            attrs = super().build_attrs(*args, **kwargs)
            attrs["data-controller"] = "polymath-textarea-controller"

            return attrs

        def _get_media_js(self):
            return super()._get_media_js() + get_polymath_config("widget")

else:
    from wagtail.telepath import register
    from wagtail.utils.widgets import WidgetWithScript
    from wagtail.widget_adapters import WidgetAdapter

    class PolymathTextareaWidget(WidgetWithScript, PolymathTextareaWidgetBase):
        def render_js_init(self, id_, name, value):
            return f'initPolymathTextareaPreview("{id_}");'

    class PolymathTextareaAdapter(WidgetAdapter):
        js_constructor = "wagtail_polymath.widgets.PolymathTextareaWidget"

        class Media:
            # TODO: remove the adapter when dropping support for Wagtail 5.2
            js = get_polymath_config("widget")

    register(PolymathTextareaAdapter(), PolymathTextareaWidget)
