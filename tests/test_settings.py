from django.test import TestCase, override_settings

from wagtail_polymath.settings import ENGINES, wagtail_polymath_settings


CUSTOM_URL = "https://example.com/mathjax/tex-mml-chtml.js"
CUSTOM_SRI = "sha256-Ynv3Q3nAtRTr6UDX+X6vbn9d1t8ZO5oV2Y4gvL9y0ck="


class TestSettings(TestCase):
    """No WAGTAIL_POLYMATH setting configured."""

    def test_default_engine(self):
        self.assertEqual(wagtail_polymath_settings.engine, "mathjax")

    @override_settings(WAGTAIL_POLYMATH={"engine": "foo"})
    def test_invalid_engine_defaults_to_mathjax(self):
        self.assertEqual(wagtail_polymath_settings.engine, "mathjax")

    def test_libraries_js(self):
        self.assertEqual(
            wagtail_polymath_settings.libraries_js, ENGINES["mathjax"]["libraries"]
        )

    @override_settings(WAGTAIL_POLYMATH={"engine": "katex"})
    def test_libraries_js_with_katex(self):
        self.assertEqual(
            wagtail_polymath_settings.libraries_js, ENGINES["katex"]["libraries"][:2]
        )

    def test_libraries_css(self):
        self.assertEqual(wagtail_polymath_settings.libraries_css, [])

    @override_settings(WAGTAIL_POLYMATH={"engine": "katex"})
    def test_libraries_css_with_katex(self):
        self.assertEqual(
            wagtail_polymath_settings.libraries_css, [ENGINES["katex"]["libraries"][2]]
        )

    @override_settings(WAGTAIL_POLYMATH={"libraries": [{"url": CUSTOM_URL}]})
    def test_libraries_js_contains_custom_url(self):
        self.assertEqual(wagtail_polymath_settings.libraries_js[0]["url"], CUSTOM_URL)

    @override_settings(WAGTAIL_POLYMATH={"libraries": [{"url": CUSTOM_URL}]})
    def test_sri_is_none(self):
        self.assertIsNone(wagtail_polymath_settings.libraries_js[0].get("sri"))

    @override_settings(
        WAGTAIL_POLYMATH={"libraries": [{"url": CUSTOM_URL, "sri": CUSTOM_SRI}]}
    )
    def test_mathjax_sri_returns_custom_sri(self):
        self.assertEqual(wagtail_polymath_settings.libraries_js[0]["sri"], CUSTOM_SRI)
