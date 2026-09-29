from django.test import TestCase, override_settings

from wagtail_polymath.settings import ENGINES, wagtail_polymath_settings
from wagtail_polymath.widgets import PolymathTextareaWidget


CUSTOM_URL = "https://example.com/mathjax/tex-mml-chtml.js"
CUSTOM_SRI = "sha256-Ynv3Q3nAtRTr6UDX+X6vbn9d1t8ZO5oV2Y4gvL9y0ck="


def widget_media_html():
    return str(PolymathTextareaWidget().media)


class TestDefaultSettings(TestCase):
    """No WAGTAIL_POLYMATH setting configured."""

    def test_libraries_returns_default(self):
        self.assertEqual(
            wagtail_polymath_settings.libraries_js, ENGINES["mathjax"]["libraries"]
        )

    def test_widget_media_uses_default_url_and_integrity(self):
        html = widget_media_html()
        default_url = ENGINES["mathjax"]["libraries"][0]["url"]
        default_sri = ENGINES["mathjax"]["libraries"][0]["sri"]
        self.assertIn(default_url, html)
        self.assertIn(f'integrity="{default_sri}"', html)
        self.assertIn('crossorigin="anonymous"', html)


@override_settings(WAGTAIL_POLYMATH={"libraries": [{"url": CUSTOM_URL}]})
class TestCustomUrlOnly(TestCase):
    """The library URL is set, no matching SRI hash supplied."""

    def test_libraries_js_contains_custom_url(self):
        self.assertEqual(wagtail_polymath_settings.libraries_js[0]["url"], CUSTOM_URL)

    def test_sri_is_none(self):
        self.assertIsNone(wagtail_polymath_settings.libraries_js[0].get("sri"))

    def test_widget_media_omits_integrity(self):
        html = widget_media_html()
        default_url = ENGINES["mathjax"]["libraries"][0]["url"]
        self.assertIn(CUSTOM_URL, html)
        self.assertNotIn(default_url, html)
        self.assertNotIn("integrity", html)
        self.assertNotIn("crossorigin", html)


@override_settings(
    WAGTAIL_POLYMATH={"libraries": [{"url": CUSTOM_URL, "sri": CUSTOM_SRI}]}
)
class TestCustomUrlAndSri(TestCase):
    """Both library url and sri are set in WAGTAIL_POLYMATH."""

    def test_mathjax_sri_returns_custom_sri(self):
        self.assertEqual(wagtail_polymath_settings.libraries_js[0]["sri"], CUSTOM_SRI)

    def test_widget_media_uses_custom_url_and_integrity(self):
        html = widget_media_html()
        self.assertIn(CUSTOM_URL, html)
        self.assertIn(f'integrity="{CUSTOM_SRI}"', html)
        self.assertIn('crossorigin="anonymous"', html)
