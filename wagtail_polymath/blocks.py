from django.forms import CharField
from django.forms.widgets import HiddenInput
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from wagtail.blocks import FieldBlock


class MathJaxWidget(HiddenInput):
    class Media:
        js = ("wagtail_polymath/js/streamfield.js",)

    template_name = "wagtail_polymath/streamfield.html"

    def get_context(self, name, value, attrs):
        context = {
            "widget": {
                "name": name,
                "is_hidden": self.is_hidden,
                "required": self.is_required,
                "value": value,
                "attrs": self.build_attrs(attrs),
                "template_name": self.template_name,
            }
        }
        return context

    def render(self, name, value, attrs=None, renderer=None):
        # id gets set, but I dont know where.
        # We need it removed so the JS will work correctly
        # attrs.pop('id')
        context = self.get_context(name, value, attrs)
        return mark_safe(render_to_string(self.template_name, context))  # noqa: S308


class MathBlock(FieldBlock):
    def __init__(self, required=True, help_text=None, **kwargs):
        self.field = CharField(
            required=required, help_text=help_text, widget=MathJaxWidget()
        )
        super().__init__(**kwargs)

    def value_from_form(self, value):
        return value
