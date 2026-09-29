from wagtail_polymath.settings import ENGINES
from wagtail_polymath.templatetags.wagtail_polymath import polymath_stylesheets


class TestStylesheetsTemplateTag:
    def test_katex_stylesheet_is_linked(self, settings):
        settings.WAGTAIL_POLYMATH = {"engine": "katex"}
        css = ENGINES["katex"]["libraries"][2]
        html = polymath_stylesheets()

        expected_output = f'<link rel="stylesheet" src="{css["url"]}" crossorigin="anonymous" integrity="{css["sri"]}" defer/>'
        assert html == expected_output

        for js in ENGINES["katex"]["libraries"][:2]:
            assert js["url"] not in html
