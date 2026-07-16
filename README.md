# wagtail-polymath

[![License: BSD-3-Clause](https://img.shields.io/badge/License-BSD--3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![PyPI version](https://img.shields.io/pypi/v/wagtailmath.svg?style=flat)](https://pypi.org/project/wagtail-polymath)
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

Install wagtail_polymath:

    pip install wagtail_polymath

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
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('equation', MathBlock())
    ])
```

Use the `mathjax_script` template tag in your front end template to load the
MathJax library:

```django+html
{% load wagtail_polymath %}
...

{% mathjax_script %}
```

## Configuration

All `wagtail-polymath` settings are defined in a single `WAGTAIL_POLYMATH`
dictionary in your settings file.

By default, wagtail-polymath loads MathJax from jsdelivr, pinned to a specific
version with a matching [Subresource Integrity](https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Subresource_Integrity)
(SRI) hash, so the browser can verify the script hasn't been tampered with.

If you'd rather load MathJax from a different CDN, your own static files, or
a different version, set `mathjax_url` to the full script URL:

```python
# settings.py
WAGTAIL_POLYMATH = {
    "mathjax_url": "https://example.com/path/to/tex-mml-chtml.js",
}
```

Since we can't know the SRI hash for a script we don't control, setting a
custom URL on its own disables integrity checking for that script (no
`integrity`/`crossorigin` attributes are rendered). If you want that
protection back, also set `mathjax_sri` to the hash for your chosen file:

```python
# settings.py
WAGTAIL_POLYMATH = {
    "mathjax_url": "https://example.com/path/to/tex-mml-chtml.js",
    "mathjax_sri": "sha256-...",
}
```

`mathjax_sri` has no effect unless `mathjax_url` is also set — the built-in
default URL always uses its own pinned hash.

Both settings apply to the MathJax script loaded in the Wagtail admin (for
the `MathBlock` live preview) and the one loaded by the `mathjax_script`
template tag. Note that the bundled preview JS assumes MathJax's combined
`tex-mml-chtml` component and its `input/asciimath` loader — if you switch to
a different version or build of MathJax, you're responsible for keeping it
compatible with that configuration.

## Contributing

All contributions are welcome! See [CONTRIBUTING.md](https://github.com/wagtail-nest/wagtail-polymath/blob/main/CONTRIBUTING.md)

Supported versions:

- Python 3.10-3.14
- Django 5.2, 6.0
- Wagtail 7.0 (LTS), 7.3, 7.4 (LTS)
