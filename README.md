# wagtail-polymath

[![License: BSD-3-Clause](https://img.shields.io/badge/License-BSD--3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![PyPI version](https://img.shields.io/pypi/v/wagtailmath.svg?style=flat)](https://pypi.org/project/wagtailmath)
[![Build status](https://img.shields.io/github/actions/workflow/status/wagtail-nest/wagtail-polymath/test.yml?branch=main)](https://github.com/wagtail-nest/wagtail-polymath/actions)

## Links

- [Documentation](https://github.com/wagtail-nest/wagtail-polymath/blob/main/README.md)
- [Changelog](https://github.com/wagtail-nest/wagtail-polymath/blob/main/CHANGELOG.md)
- [Contributing](https://github.com/wagtail-nest/wagtail-polymath/blob/main/CONTRIBUTING.md)
- [Discussions](https://github.com/wagtail-nest/wagtail-polymath/discussions)
- [Security](https://github.com/wagtail-nest/wagtail-polymath/security)

`wagtail-polymath` provides robust math typesetting capabilities in LaTeX syntax.
This project supports multiple typesetting engines, including MathJax and KaTeX, allowing users to choose the one that best fits their needs.

- [LaTeX Syntax Support](https://en.wikibooks.org/wiki/LaTeX/Mathematics): Write complex mathematical expressions using familiar LaTeX syntax.
- Multiple Typesetting Engines: Currently, [MathJax](https://www.mathjax.org/) (default) and [KaTeX](https://katex.org/) are supported.
- Live preview.

![](https://github.com/wagtail-nest/wagtail-polymath/blob/main/docs/images/mathblock.png)

## Quickstart

Install wagtail-polymath:

    pip install wagtail-polymath

Add it to your `INSTALLED_APPS`:

```python
# settings.py

INSTALLED_APPS = (
    # ...
    "wagtail_polymath",
    # ...
)
```

Use `MathBlock` in your `StreamField` content:

```python
from wagtail_polymath.blocks import MathBlock

class MyPage(Page):
    body = StreamField(
        [
            ('heading', blocks.CharBlock(classname="full title")),
            ('paragraph', blocks.RichTextBlock()),
            ('equation', MathBlock())
        ],
        use_json_field=True,
    )

    content_panels = Page.content_panels + [FieldPanel("body")]
```

Use the `polymath_js` template tag in your front-end template to load the typesetting library:

```django+html
{% load wagtail_polymath %}

{# include this line in css block #}
{% polymath_css %}

{# include this line in js block #}
{% polymath_js %}
```

Now you can use LaTeX syntax in your StreamField editor to create mathematical expressions.
By default, `wagtail-polymath` uses MathJax for rendering, but KaTeX is also supported (see below).

## Settings

### WAGTAILPOLYMATH_ENGINE

If you wants to use KaTeX instead of MathJax, simply add the following line to your Django settings:

```python
WAGTAILPOLYMATH_ENGINE = "katex"
```

This value is set to "mathjax" by default.

### WAGTAILPOLYMATH_SETTINGS

For those who want to specify the CDN provider or for internal site hosting.
The rendering javascript library path can be customized for different use cases.

Default settings for `MathJax`:

```python
WAGTAILPOLYMATH_SETTINGS = {
    "js": [
        "https://cdn.jsdelivr.net/npm/mathjax@2/MathJax.js?config=TeX-MML-AM_CHTML",
    ],
}
```

Default settings for `KaTeX`:

```python
WAGTAILPOLYMATH_SETTINGS = {
    "js": [
        "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js",
        "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js",
    ],
    "css": ["https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css"],
}
```

## Migration from `wagtail-math`

- Django settings:
  - Replace "wagtailmath" with "wagtail_polymath" in `INSTALLED_APPS`
- Import section:
  - Replace "from wagtailmath.blocks import MathBlock" with "from wagtail_polymath.blocks import MathBlock"
- HTML template:
  - Replace "wagtailmath" with "wagtail_polymath" in the load section
  - Add "{% polymath_css %}" to the css block
  - Replace "<script src={% mathjax %}></script>" with "{% polymath_js %}" in the js block

## Contributing

All contributions are welcome! See [CONTRIBUTING.md](https://github.com/wagtail-nest/wagtail-polymath/blob/main/CONTRIBUTING.md)

Supported versions:

- Python 3.8, 3.9, 3.10, 3.11, 3.12
- Django 4.2, 5.0
- Wagtail 5.2 (LTS), 6.0, 6.1
