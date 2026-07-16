from wagtail_polymath.settings import (
    MATHJAX_DEFAULT_SRI,
    MATHJAX_DEFAULT_URL,
    wagtail_polymath_settings,
)
from wagtail_polymath.templatetags.wagtail_polymath import mathjax_script
from wagtail_polymath.widgets import MathJaxWidget


CUSTOM_URL = "https://example.com/mathjax/tex-mml-chtml.js"
CUSTOM_SRI = "sha256-Ynv3Q3nAtRTr6UDX+X6vbn9d1t8ZO5oV2Y4gvL9y0ck="


def widget_media_html():
    return str(MathJaxWidget().media)


class TestDefaultMathJaxSettings:
    """No WAGTAIL_POLYMATH setting configured."""

    def test_mathjax_url_returns_default(self):
        assert wagtail_polymath_settings.mathjax_url == MATHJAX_DEFAULT_URL

    def test_mathjax_sri_returns_default(self):
        assert wagtail_polymath_settings.mathjax_sri == MATHJAX_DEFAULT_SRI

    def test_widget_media_uses_default_url_and_integrity(self):
        html = widget_media_html()
        assert MATHJAX_DEFAULT_URL in html
        assert f'integrity="{MATHJAX_DEFAULT_SRI}"' in html
        assert 'crossorigin="anonymous"' in html

    def test_template_tag_uses_default_url_and_integrity(self):
        html = mathjax_script()
        assert MATHJAX_DEFAULT_URL in html
        assert f'integrity="{MATHJAX_DEFAULT_SRI}"' in html
        assert 'crossorigin="anonymous"' in html


class TestCustomUrlOnly:
    """WAGTAIL_POLYMATH["mathjax_url"] set, no matching SRI hash supplied."""

    def test_mathjax_url_returns_custom_url(self, settings):
        settings.WAGTAIL_POLYMATH = {"mathjax_url": CUSTOM_URL}
        assert wagtail_polymath_settings.mathjax_url == CUSTOM_URL

    def test_mathjax_sri_is_none(self, settings):
        settings.WAGTAIL_POLYMATH = {"mathjax_url": CUSTOM_URL}
        assert wagtail_polymath_settings.mathjax_sri is None

    def test_widget_media_omits_integrity(self, settings):
        settings.WAGTAIL_POLYMATH = {"mathjax_url": CUSTOM_URL}
        html = widget_media_html()
        assert CUSTOM_URL in html
        assert MATHJAX_DEFAULT_URL not in html
        assert "integrity" not in html
        assert "crossorigin" not in html

    def test_template_tag_omits_integrity(self, settings):
        settings.WAGTAIL_POLYMATH = {"mathjax_url": CUSTOM_URL}
        html = mathjax_script()
        assert CUSTOM_URL in html
        assert "integrity" not in html
        assert "crossorigin" not in html


class TestCustomUrlAndSri:
    """Both mathjax_url and mathjax_sri set in WAGTAIL_POLYMATH."""

    def test_mathjax_sri_returns_custom_sri(self, settings):
        settings.WAGTAIL_POLYMATH = {
            "mathjax_url": CUSTOM_URL,
            "mathjax_sri": CUSTOM_SRI,
        }
        assert wagtail_polymath_settings.mathjax_sri == CUSTOM_SRI

    def test_widget_media_uses_custom_url_and_integrity(self, settings):
        settings.WAGTAIL_POLYMATH = {
            "mathjax_url": CUSTOM_URL,
            "mathjax_sri": CUSTOM_SRI,
        }
        html = widget_media_html()
        assert CUSTOM_URL in html
        assert f'integrity="{CUSTOM_SRI}"' in html
        assert 'crossorigin="anonymous"' in html

    def test_template_tag_uses_custom_url_and_integrity(self, settings):
        settings.WAGTAIL_POLYMATH = {
            "mathjax_url": CUSTOM_URL,
            "mathjax_sri": CUSTOM_SRI,
        }
        html = mathjax_script()
        assert CUSTOM_URL in html
        assert f'integrity="{CUSTOM_SRI}"' in html
        assert 'crossorigin="anonymous"' in html

    def test_sri_ignored_without_matching_url(self, settings):
        """The mathjax_sri key alone (no mathjax_url) must not affect the default."""
        settings.WAGTAIL_POLYMATH = {"mathjax_sri": CUSTOM_SRI}
        assert wagtail_polymath_settings.mathjax_url == MATHJAX_DEFAULT_URL
        assert wagtail_polymath_settings.mathjax_sri == MATHJAX_DEFAULT_SRI
