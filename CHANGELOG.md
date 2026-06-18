# wagtail-polymath Changelog

## Unreleased

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
