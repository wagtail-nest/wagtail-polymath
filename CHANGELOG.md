# wagtail-polymath Changelog

## Unreleased

- Dropped support for Django < 5.2
- Upgraded to MathJax 4.1.2, using [Subresource Integrity](https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Subresource_Integrity)
  for the CDN script. The template tag has also changed to `mathjax_script`. See upgrade considerations
- Added a `WAGTAIL_POLYMATH` settings dict, with `mathjax_url` and `mathjax_sri` keys, to allow
  loading MathJax from a different CDN, or self-hosted, instead of the pinned jsdelivr default.
  See [Configuration](README.md#configuration)

### Upgrade considerations

#### The project namespace changed to `wagtail_polymath`

```diff
# Old
- from wagtailmath.blocks import MathBlock
# New
+ from wagtail_polymath.blocks import MathBlock
```

and

```diff
# Old
- {% load wagtailmath %}
# New
+ {% load wagtail_polymath %}
```

#### The template tag has changed
The `mathjax` template tag has changed to `mathjax_script` and should no longer be wrapped in `<script></script>`

```diff
# Old
- {% load wagtailmath %}
- <script src="{% mathjax %}"></script>
# New
+ {% load wagtail_polymath %}
+ {% mathjax_script %}
```

#### `MATHJAX_VERSION`/`MATHJAX_SRI` moved out of `widgets.py`
These were never documented as public API, but if you imported them
directly, they now live in `wagtail_polymath.settings`, which also exposes
a `wagtail_polymath_settings` object (`.mathjax_url`/`.mathjax_sri`) for
reading the effective, resolved settings.

## 2.0.0.dev1 (2026-06-18)

- The project namespace has changed from wagtailmath to wagtail_polymath.
  Example: `from wagtailmath.blocks import MathBlock` → `from wagtail_polymath.blocks import MathBlock`

## 1.3.1 (2024-10-30)

- Fixed preview initialisation issue (#17) @MadScrewdriver

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
