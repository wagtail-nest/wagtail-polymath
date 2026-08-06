from django import template

from wagtailmath.settings import wagtail_polymath_settings


register = template.Library()


@register.simple_tag
def mathjax(config="TeX-MML-AM_CHTML"):
    """
    Return the URL of the MathJax library to load on the front end.

    PORT NOTE: ``config`` no longer has any effect. The URL now comes from a
    single setting that carries its own ``?config=``, and appending to a URL we
    don't control would break any that already have a query string. The
    argument is kept so that existing ``{% mathjax config="..." %}`` templates
    don't raise TypeError; see the 1.4.0 upgrade considerations.

    PORT NOTE: 2.x's equivalent tag returns a full ``<script>`` element and so
    can apply ``mathjax_sri``. This one returns a bare URL, so
    ``integrity``/``crossorigin`` are the caller's responsibility and
    ``mathjax_sri`` only affects the admin widget.
    """
    return wagtail_polymath_settings.mathjax_url
