# wagtail-polymath Changelog

## Unreleased

## 1.4.0 (2026-08-06)

- Dropped support for Python < 3.10, Django < 5.2, Wagtail < 7.0
- Added a `WAGTAIL_POLYMATH` settings dict, with `mathjax_url` and `mathjax_sri` keys, to allow
  loading MathJax from a different CDN, or self-hosted, instead of the pinned cdnjs default.
  See [Configuration](README.md#configuration)
- The MathJax script loaded in the Wagtail admin now uses
  [Subresource Integrity](https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Subresource_Integrity),
  so the browser can verify the script hasn't been tampered with

### Upgrade considerations

#### The `mathjax` template tag ignores its `config` argument

The MathJax URL now comes from a single setting, which carries its own
`?config=` query parameter, so there is nothing for the tag to append to.
`{% mathjax config="..." %}` still works but the argument has no effect, and
the front end now loads the same `TeX-MML-AM_HTMLorMML` configuration the
admin has always used, rather than `TeX-MML-AM_CHTML`. To load a different
MathJax configuration, set `mathjax_url` to a URL with the `?config=` you want.

#### `MATHJAX_VERSION` moved out of `widgets.py`

This was never documented as public API, but if you imported it directly, it
now lives in `wagtailmath.settings`, which also exposes a
`wagtail_polymath_settings` object (`.mathjax_url`/`.mathjax_sri`) for reading
the effective, resolved settings.

#### `integrity` and `crossorigin` are now set on the admin MathJax script

If you proxy or rewrite the MathJax script in the Wagtail admin, the browser
will now reject it unless the bytes match the pinned hash. Set `mathjax_url`
to your own URL, which turns integrity checking off unless you also supply a
matching `mathjax_sri`.

## 1.3.1 (2024-10-30)

- Fixed preview initialisation issue (https://github.com/wagtail-nest/wagtail-polymath/pull/17) @MadScrewdriver

## 1.3.0 (2024-07-04)

- Updated project tooling:
  - added linting with ruff
  - switched to using flit for packaging
  - added GitHub Actions, including PyPI trusted publishing
  - added tests skeleton
- Added support for Wagtail 5.2+
- Dropped support for Wagtail < 5.2, Django < 4.2

## 1.2.0 (2021-05-18)

-   Upgrade to newer version of Django + Wagtail

## 0.1.0 (2017-04-24)

-   First release on PyPI.
