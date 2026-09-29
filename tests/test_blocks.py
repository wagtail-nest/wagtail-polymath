from django import forms
from django.test import TestCase

from wagtail_polymath.blocks import MathBlock
from wagtail_polymath.widgets import PolymathTextareaWidget


class TestPolymathTextareaWidget(TestCase):
    def test_block(self):
        block = MathBlock()

        self.assertIsInstance(block.field, forms.CharField)
        self.assertIsInstance(block.field.widget, PolymathTextareaWidget)
