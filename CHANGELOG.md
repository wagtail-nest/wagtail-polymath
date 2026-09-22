# wagtail-polymath Changelog

## Unreleased

- Dropped support for Django < 5.2
- Upgraded to MathJax 4.1.2, using [Subresource Integrity](https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Subresource_Integrity)
  for the CDN script. The template tag has also changed to `polymath_scripts`. See the upgrade considerations
- Added support for the [KaTeX](https://katex.org/) typesetting library
- Added a `WAGTAIL_POLYMATH` settings dict, with `libraries` list of `url` (required) and `sri` (optional) keys,
  to allow loading the preferred typesetting library (MathJax/KaTeX) from a different CDN, or self-hosted service,
  instead of the pinned jsDelivr default. See [Configuration](README.md#configuration)

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
The `mathjax` template tag has changed to `polymath_scripts` and should no longer be wrapped in `<script></script>`

```diff
# Old
- {% load wagtailmath %}
- <script src="{% mathjax %}"></script>
# New
+ {% load wagtail_polymath %}
+ {% polymath_scripts %}
```

additionally, there is a new templated tag to use for stylesheets, if you're using KaTeX. `{% polymath_stylesheets %}`

#### `MATHJAX_VERSION`/`MATHJAX_SRI` moved out of `widgets.py`
These were never documented as public API. `MATHJAX_VERSION` now lives in `wagtail_polymath.settings`.

#### Configuration via the `WAGTAIL_POLYMATH` setting dictionary
Configuration is now done via the `WAGTAIL_POLYMATH` setting dictionary.

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

## 2.0.0.dev1 (2026-06-18)

- The project namespace has changed from `wagtailmath` to `wagtail_polymath`.
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
