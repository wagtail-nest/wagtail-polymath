from django import forms
from django.forms.utils import flatatt
from django.utils.html import format_html
from wagtail import VERSION as WAGTAIL_VERSION
from wagtail.admin.staticfiles import versioned_static

from .settings import wagtail_polymath_settings


class Script:
    """
    A script in form media, rendered with extra attributes.

    PORT NOTE: 2.x uses ``django.forms.Script`` for this. That class only
    exists from Django 5.2 and this release line still supports Django 4.2 and
    5.0, so we need our own. ``Media.render_js`` has rendered media items via
    ``__html__()`` since Django 4.2, so the output matches what 2.x produces.
    """

    def __init__(self, src, **attributes):
        self.src = src
        self.attributes = attributes

    def __html__(self):
        return format_html(
            '<script src="{src}"{attributes}></script>',
            src=self.src,
            attributes=flatatt(self.attributes),
        )

    def __str__(self):
        return self.src

    # Media.merge() collects items into an OrderedSet and a dependency graph,
    # so these are both required: without __hash__ merging raises TypeError,
    # and without __eq__ two equivalent Script objects from different widgets
    # render the same CDN script twice on a page with several MathBlocks.
    def __eq__(self, other):
        if isinstance(other, Script):
            return self.src == other.src and self.attributes == other.attributes
        return NotImplemented

    def __hash__(self):
        return hash((self.src, tuple(sorted(self.attributes.items()))))


class MathJaxWidgetBase(forms.Textarea):
    template_name = "wagtailmath/mathjaxwidget.html"

    def _get_media_js(self):
        # PORT NOTE: 2.x also passes defer=True here. We can't: wagtailmath.js
        # and the Stimulus controller are not deferred, and
        # initMathJaxPreview() calls MathJax.Callback() as soon as it runs, so
        # deferring only the CDN script would leave MathJax undefined at that
        # point and break the live preview.
        attributes = {}
        integrity = wagtail_polymath_settings.mathjax_sri
        if integrity:
            attributes["crossorigin"] = "anonymous"
            attributes["integrity"] = integrity

        return (
            Script(wagtail_polymath_settings.mathjax_url, **attributes),
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
