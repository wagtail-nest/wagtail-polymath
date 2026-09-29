from django import forms
from django.utils.functional import cached_property
from wagtail.blocks import TextBlock

from .widgets import PolymathTextareaWidget


class MathBlock(TextBlock):
    @cached_property
    def field(self):
        field_kwargs = {"widget": PolymathTextareaWidget(attrs={"rows": self.rows})}
        field_kwargs.update(self.field_options)
        return forms.CharField(**field_kwargs)
