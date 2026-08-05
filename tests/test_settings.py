from wagtailmath.settings import (
    MATHJAX_DEFAULT_SRI,
    MATHJAX_DEFAULT_URL,
    wagtail_polymath_settings,
)
from wagtailmath.templatetags.wagtailmath import mathjax
from wagtailmath.widgets import MathJaxWidget


CUSTOM_URL = "https://example.com/mathjax/MathJax.js"
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

    # PORT NOTE: 2.x asserts on integrity/crossorigin in the template tag output
    # too. This tag returns a bare URL, so there are no attributes to assert on.
    def test_template_tag_uses_default_url(self):
        assert mathjax() == MATHJAX_DEFAULT_URL

    # Addition beyond the backported change: 2.x has no test for the config
    # argument, because its tag doesn't take one.
    def test_template_tag_ignores_config_argument(self):
        assert mathjax(config="TeX-MML-AM_CHTML") == MATHJAX_DEFAULT_URL


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

    def test_template_tag_returns_custom_url(self, settings):
        settings.WAGTAIL_POLYMATH = {"mathjax_url": CUSTOM_URL}
        assert mathjax() == CUSTOM_URL


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

    def test_template_tag_returns_custom_url(self, settings):
        settings.WAGTAIL_POLYMATH = {
            "mathjax_url": CUSTOM_URL,
            "mathjax_sri": CUSTOM_SRI,
        }
        assert mathjax() == CUSTOM_URL

    def test_sri_ignored_without_matching_url(self, settings):
        """The mathjax_sri key alone (no mathjax_url) must not affect the default."""
        settings.WAGTAIL_POLYMATH = {"mathjax_sri": CUSTOM_SRI}
        assert wagtail_polymath_settings.mathjax_url == MATHJAX_DEFAULT_URL
        assert wagtail_polymath_settings.mathjax_sri == MATHJAX_DEFAULT_SRI


class TestInvalidSettings:
    """
    Addition beyond the backported change: 2.x guards against a non-dict
    WAGTAIL_POLYMATH in _user_settings but doesn't test that branch.
    """

    def test_non_dict_setting_falls_back_to_defaults(self, settings):
        settings.WAGTAIL_POLYMATH = "not-a-dict"
        assert wagtail_polymath_settings.mathjax_url == MATHJAX_DEFAULT_URL
        assert wagtail_polymath_settings.mathjax_sri == MATHJAX_DEFAULT_SRI

    def test_empty_dict_falls_back_to_defaults(self, settings):
        settings.WAGTAIL_POLYMATH = {}
        assert wagtail_polymath_settings.mathjax_url == MATHJAX_DEFAULT_URL
        assert wagtail_polymath_settings.mathjax_sri == MATHJAX_DEFAULT_SRI


class TestScriptDeduplication:
    """
    Addition beyond the backported change, covering the local Script class that
    stands in for django.forms.Script on Django < 5.2. Django's Media.merge()
    collects items into an OrderedSet and a dependency graph, so Script has to
    be both hashable and comparable or merging two widgets' media either raises
    TypeError or renders the CDN script twice.
    """

    def test_merged_widget_media_renders_cdn_script_once(self):
        combined = str(MathJaxWidget().media + MathJaxWidget().media)
        assert combined.count(MATHJAX_DEFAULT_URL) == 1
