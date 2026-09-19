from wagtail_polymath.settings import ENGINES, wagtail_polymath_settings
from wagtail_polymath.templatetags.wagtail_polymath import mathjax_script
from wagtail_polymath.widgets import PolymathTextareaWidget


CUSTOM_URL = "https://example.com/mathjax/tex-mml-chtml.js"
CUSTOM_SRI = "sha256-Ynv3Q3nAtRTr6UDX+X6vbn9d1t8ZO5oV2Y4gvL9y0ck="


def widget_media_html():
    return str(PolymathTextareaWidget().media)


class TestDefaultMathJaxSettings:
    """No WAGTAIL_POLYMATH setting configured."""

    def test_libraries_returns_default(self):
        assert wagtail_polymath_settings.libraries_js == ENGINES["mathjax"]["libraries"]

    def test_widget_media_uses_default_url_and_integrity(self):
        html = widget_media_html()
        default_url = ENGINES["mathjax"]["libraries"][0]["url"]
        default_sri = ENGINES["mathjax"]["libraries"][0]["sri"]
        assert default_url in html
        assert f'integrity="{default_sri}"' in html
        assert 'crossorigin="anonymous"' in html

    def test_template_tag_uses_default_url_and_integrity(self):
        html = mathjax_script()
        default_url = ENGINES["mathjax"]["libraries"][0]["url"]
        default_sri = ENGINES["mathjax"]["libraries"][0]["sri"]
        assert default_url in html
        assert f'integrity="{default_sri}"' in html
        assert 'crossorigin="anonymous"' in html


class TestCustomUrlOnly:
    """The library URL is set, no matching SRI hash supplied."""

    def test_mathjax_url_returns_custom_url(self, settings):
        settings.WAGTAIL_POLYMATH = {"libraries": [{"url": CUSTOM_URL}]}
        assert wagtail_polymath_settings.libraries_js[0]["url"] == CUSTOM_URL

    def test_mathjax_sri_is_none(self, settings):
        settings.WAGTAIL_POLYMATH = {"libraries": [{"url": CUSTOM_URL}]}
        assert wagtail_polymath_settings.libraries_js[0].get("sri") is None

    def test_widget_media_omits_integrity(self, settings):
        settings.WAGTAIL_POLYMATH = {"libraries": [{"url": CUSTOM_URL}]}
        html = widget_media_html()
        default_url = ENGINES["mathjax"]["libraries"][0]["url"]
        assert CUSTOM_URL in html
        assert default_url not in html
        assert "integrity" not in html
        assert "crossorigin" not in html

    def test_template_tag_omits_integrity(self, settings):
        settings.WAGTAIL_POLYMATH = {"libraries": [{"url": CUSTOM_URL}]}
        html = mathjax_script()
        assert CUSTOM_URL in html
        assert "integrity" not in html
        assert "crossorigin" not in html


class TestCustomUrlAndSri:
    """Both mathjax_url and mathjax_sri set in WAGTAIL_POLYMATH."""

    def test_mathjax_sri_returns_custom_sri(self, settings):
        settings.WAGTAIL_POLYMATH = {
            "libraries": [{"url": CUSTOM_URL, "sri": CUSTOM_SRI}]
        }
        assert wagtail_polymath_settings.libraries_js[0]["sri"] == CUSTOM_SRI

    def test_widget_media_uses_custom_url_and_integrity(self, settings):
        settings.WAGTAIL_POLYMATH = {
            "libraries": [{"url": CUSTOM_URL, "sri": CUSTOM_SRI}]
        }
        html = widget_media_html()
        assert CUSTOM_URL in html
        assert f'integrity="{CUSTOM_SRI}"' in html
        assert 'crossorigin="anonymous"' in html

    def test_template_tag_uses_custom_url_and_integrity(self, settings):
        settings.WAGTAIL_POLYMATH = {
            "libraries": [{"url": CUSTOM_URL, "sri": CUSTOM_SRI}]
        }
        html = mathjax_script()
        assert CUSTOM_URL in html
        assert f'integrity="{CUSTOM_SRI}"' in html
        assert 'crossorigin="anonymous"' in html
