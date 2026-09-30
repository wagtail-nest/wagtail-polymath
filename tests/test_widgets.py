from django.test import TestCase, override_settings

from wagtail_polymath.settings import ENGINES
from wagtail_polymath.widgets import PolymathTextareaWidget


CUSTOM_URL = "https://example.com/mathjax/tex-mml-chtml.js"
CUSTOM_SRI = "sha256-Ynv3Q3nAtRTr6UDX+X6vbn9d1t8ZO5oV2Y4gvL9y0ck="


class TestPolymathTextareaWidget(TestCase):
    def setUp(self) -> None:
        self.widget = PolymathTextareaWidget()

    def test_widget_build_attr(self):
        attrs = self.widget.build_attrs({})
        self.assertEqual(attrs["data-controller"], "polymath-textarea-controller")

    def test_widget_media(self):
        default_url = ENGINES["mathjax"]["libraries"][0]["url"]
        default_sri = ENGINES["mathjax"]["libraries"][0]["sri"]
        self.assertInHTML(
            f'<script src="{default_url}" integrity="{default_sri}" crossorigin="anonymous" defer></script>',
            str(self.widget.media),
        )

    @override_settings(WAGTAIL_POLYMATH={"engine": "katex"})
    def test_widget_media_contains_css_if_set(self):
        css = ENGINES["katex"]["libraries"][2]
        self.assertInHTML(
            f'<link rel="stylesheet" media="all" href="{css["url"]}" crossorigin="anonymous" integrity="{css["sri"]}" />',
            str(self.widget.media),
        )

    @override_settings(WAGTAIL_POLYMATH={"libraries": [{"url": CUSTOM_URL}]})
    def test_widget_media_omits_integrity_if_not_set(self):
        html = str(self.widget.media)
        default_url = ENGINES["mathjax"]["libraries"][0]["url"]
        self.assertIn(CUSTOM_URL, html)
        self.assertNotIn(default_url, html)
        self.assertNotIn("integrity", html)
        self.assertNotIn("crossorigin", html)

    @override_settings(
        WAGTAIL_POLYMATH={"libraries": [{"url": CUSTOM_URL, "sri": CUSTOM_SRI}]}
    )
    def test_widget_media_uses_custom_url_and_integrity(self):
        self.assertInHTML(
            f'<script src="{CUSTOM_URL}" integrity="{CUSTOM_SRI}" crossorigin="anonymous" defer></script>',
            str(self.widget.media),
        )
