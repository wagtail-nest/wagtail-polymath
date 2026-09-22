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

wagtail-polymath allows you to write equations in your[Wagtail](https://github.com/wagtail/wagtail) content using markup
and render them beautifully.

wagtail-polymath provides a `MathBlock` so you can write equations in markup (TeX, MathML, ASCIIMath) and render them
with a typesetting engine (MathJax or KaTeX), with MathJax being the default. It features a live preview:

![](https://github.com/wagtail-nest/wagtail-polymath/blob/main/docs/images/mathblock.png)

`MathBlock` uses MathJax for rendering so there is very little to do on
the front end. Include the chosen typesetting engine JavaScript (and optionally CSS), and render the raw
`MathBlock` content as you would for any other streamfield plain text block.

wagtail-polymath includes a template tag to include the chosen typesetting engine library files for you from a CDN.
MathJax is configured to accept all recognised markup (TeX, MathML, ASCIIMath) and renders them to HTML.

For help on using the markup languages see the relevant MathJax
documentation (e.g. https://docs.mathjax.org/en/latest/input/tex/index.html) and
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
from wagtail import blocks
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail_polymath.blocks import MathBlock


class MyPage(Page):
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('equation', MathBlock())
    ])
```

Use the `polymath_scripts` template tag in your front-end template to load the typesetting library:

```django+html
{% load wagtail_polymath %}
...

{% polymath_scripts %}
```

> [!Note]
> The KaTeX typesetting engine provides additional CSS that needs to be included using the `{% polymath_stylesheets %}`
> template tag.

## Configuration

All `wagtail-polymath` settings are defined in a single `WAGTAIL_POLYMATH`dictionary in your settings file.

```python
# settings.py
WAGTAIL_POLYMATH = {
    "engine": "mathjax",  # Optional. Allowed values: "mathjax", "katex". Defaults to "mathjax",
    "libraries": [
        {
            "url": "...",  # Required. A fully qualified URL
            "sri": "...",  # Optional. The Subresource Integrity hash
        },
        ...
    ]
}
```

By default, wagtail-polymath loads the typesetting library from jsDelivr, pinned to a specific
version with a matching [Subresource Integrity](https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Subresource_Integrity)
(SRI) hash, so the browser can verify the script hasn't been tampered with.

If you'd rather load the typesetting library from a different CDN, your own static files, or
a different version, set the relevant entries`library_url` to the full script URL:

```python
# settings.py
WAGTAIL_POLYMATH = {
    "libraries": [
        {"url": "https://example.com/path/to/tex-mml-chtml.js"},
    ]
}
```

Since we can't know the SRI hash for a script we don't control, setting a custom URL on its own disables integrity
checking for that script (no `integrity`/`crossorigin` attributes are rendered). If you want that protection back,
set `sri` to the hash for your chosen file:

```python
# settings.py
WAGTAIL_POLYMATH = {
    "libraries": [
        {
            "url": "https://example.com/path/to/tex-mml-chtml.js",
            "sri": "sha256-...",
        }
    ]
}
```

The `sri` has no effect unless `url` is also set — the built-in default URL always uses its own pinned hash.

To generate the hash for your chosen file, download it and use `openssl`.
Note that the `integrity` attribute requires a **base64**-encoded digest —
`sha256sum`/`shasum` produce a hex digest instead, which will not work:

```sh
openssl dgst -sha256 -binary tex-mml-chtml.js | openssl base64 -A
```

Prefix the output with `sha256-` to get the full `library_sri` value:

```python
WAGTAIL_POLYMATH = {
    "libraries": [
        {
            "url": "https://example.com/path/to/tex-mml-chtml.js",
            "sri": "sha256-dPV35kaoLq1rg+JbYf8p1kTrZamwMY+XIwaWUPwqtpU=",
        }
    ]
}
```

Both settings apply to the typesetting script loaded in the Wagtail admin (for the `MathBlock` live preview)
and the one loaded by the `polymath_scripts` template tag.

Note that if you are using MathJax, the bundled preview JS assumes MathJax's combined `tex-mml-chtml` component and
its `input/asciimath` loader — if you switch to a different version or build of MathJax, you're responsible for keeping
it compatible with that configuration.

## Contributing

All contributions are welcome! See [CONTRIBUTING.md](https://github.com/wagtail-nest/wagtail-polymath/blob/main/CONTRIBUTING.md)

Supported versions:

- Python 3.10-3.14
- Django 5.2, 6.0
- Wagtail 7.0 (LTS), 7.3, 7.4 (LTS)
