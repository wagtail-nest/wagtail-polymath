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

wagtail-polymath allows you to write equations in your
[Wagtail](https://github.com/wagtail/wagtail) content using markup and
render them beautifully.

wagtail-polymath provides a `MathBlock` so you can write equations in markup
(TeX, MathML, ASCIIMath) and render them with MathJax. It features a
live preview:

![](https://github.com/wagtail-nest/wagtail-polymath/blob/main/docs/images/mathblock.png)

`MathBlock` uses MathJax for rendering so there is very little to do on
the front end. Simply include the MathJax JS and render the raw
`MathBlock` content as you would for any other streamfield plain text
block.

wagtail-polymath even includes a template tag to include the MathJax JS for
you from a CDN. By default, MathJax is configured to accept all
recognised markup (TeX, MathML, ASCIIMath) and renders them to HTML. To
change the configuration, you can pass the desired config command to the
templatetag. See the [MathJax documentation](https://docs.mathjax.org/en/v2.7-latest/config-files.html#combined-configurations)
for possible configurations.

For help on using the markup languages see the relevant MathJax
documentation (e.g. https://docs.mathjax.org/en/v2.7-latest/tex.html) and
the markup language-specific documentation (e.g. https://en.wikibooks.org/wiki/LaTeX)

## Quickstart

Install wagtailmath:

    pip install wagtailmath

Add it to your `INSTALLED_APPS`:

```python
# settings.py

INSTALLED_APPS = (
    # ...
    "wagtailmath",
    # ...
)
```

Use `MathBlock` in your `StreamField` content:

```python
from wagtailmath.blocks import MathBlock

class MyPage(Page):
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('equation', MathBlock())
    ])
```

Use the `mathjax` template tag in your front end template to load the
MathJax library:

```django+html
{% load wagtailmath %}
...

<script src="{% mathjax %}"></script>
```


## Contributing

All contributions are welcome! See [CONTRIBUTING.md](https://github.com/wagtail-nest/wagtail-polymath/blob/main/CONTRIBUTING.md)

Supported versions:

- Python 3.8, 3.9, 3.10, 3.11, 3.12
- Django 4.2, 5.0
- Wagtail 5.2 (LTS), 6.0, 6.1
