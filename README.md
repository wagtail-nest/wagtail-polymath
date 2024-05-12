# Wagtail polymath

Math typesetting for Wagtail CMS

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/wagtail-polymath.svg)](https://badge.fury.io/py/wagtail-polymath)
[![polymath CI](https://github.com/wagtail-nest/wagtail-polymath/actions/workflows/test.yml/badge.svg)](https://github.com/wagtail-nest/wagtail-polymath/actions/workflows/test.yml)

wagtail-polymath allows you to write equations in your `Wagtail <https://github.com/wagtail/wagtail>`_ content using markup and render them beautifully.

wagtail-polymath provides a `MathBlock` so you can write equations in markup (TeX, MathML, ASCIIMath) and render them with MathJax.
It features a live preview:

![MathBlock in the Wagtail admin](https://raw.githubusercontent.com/wagtail-nest/wagtail-polymath/rename/screenshots/mathblock.png)

`MathBlock` uses MathJax for rendering so there is very little to do on the front end. Simply include
the MathJax JS and render the raw `MathBlock` content as you would for any other streamfield plain text block.

wagtail-polymath even includes a template tag to include the MathJax JS for you from a CDN.
By default, MathJax is configured to accept all recognised markup (TeX, MathML, ASCIIMath) and renders them to HTML.
To change the configuration, you can pass the desired config command to the templatetag.
See http://docs.mathjax.org/en/latest/config-files.html#combined-configurations for possible configurations.

For help on using the markup languages see the relevant MathJax documentation (e.g. http://docs.mathjax.org/en/latest/tex.html)
and the markup language-specific documentation (e.g. https://en.wikibooks.org/wiki/LaTeX)

## Links

- [Documentation](https://github.com/wagtail-nest/wagtail-polymath/blob/main/README.md)
- [Changelog](https://github.com/wagtail-nest/wagtail-polymath/blob/main/CHANGELOG.md)
- [Contributing](https://github.com/wagtail-nest/wagtail-polymath/blob/main/CONTRIBUTING.md)
- [Discussions](https://github.com/wagtail-nest/wagtail-polymath/discussions)
- [Security](https://github.com/wagtail-nest/wagtail-polymath/security)

## Quickstart

Install wagtail-polymath:

```sh
pip install wagtail-polymath
```

Add it to your `INSTALLED_APPS`:


```python
INSTALLED_APPS = [
    ...
    "wagtail_polymath",
    ...
]
```

Use `MathBlock` in your `StreamField` content:

```python
from wagtail_polymath.blocks import MathBlock

class MyPage(Page):
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('equation', MathBlock())
    ])
```

Load required CSS and JS in HTML template:

```html
{% load wagtail_polymath %}
...

{% block extra_css %}
{% wagtail_polymath_css %}
...
{% endblock extra_css %}

...
{% block extra_js %}
{% wagtail_polymath_js %}
...
{% endblock extra_js %}
```
