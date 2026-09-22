from typing import TYPE_CHECKING, Any

from django import template
from django.forms.utils import flatatt
from django.utils.html import format_html, format_html_join
from wagtail.admin.staticfiles import versioned_static

from wagtail_polymath.settings import wagtail_polymath_settings


if TYPE_CHECKING:
    from django.utils.safestring import SafeString

    from wagtail_polymath.settings import LibraryDict

register = template.Library()


def _build_attributes(
    library: "LibraryDict", defer: bool = True
) -> dict[str, str | bool]:
    attrs = {}
    if defer:
        attrs["defer"] = True

    if sri := library.get("sri", "").strip():
        attrs["crossorigin"] = "anonymous"
        attrs["integrity"] = sri

    return attrs


@register.simple_tag
def polymath_scripts() -> "Any | SafeString":
    scripts = []
    if wagtail_polymath_settings.init_js:
        scripts.append(
            format_html(
                '<script src="{init_path}"></script>',
                init_path=versioned_static(wagtail_polymath_settings.init_js),
            )
        )
    for library in wagtail_polymath_settings.libraries_js:
        attributes = _build_attributes(library)
        scripts.append(
            format_html(
                '<script src="{path}"{attributes}></script>',
                path=library["url"],
                attributes=flatatt(attributes),
            )
        )

    return format_html_join("\n", "{}", [(script,) for script in scripts])


@register.simple_tag
def polymath_stylesheets() -> "Any | SafeString":
    stylesheets = []
    for library in wagtail_polymath_settings.libraries_js:
        attributes = _build_attributes(library)
        stylesheets.append(
            format_html(
                '<link rel="stylesheet" src="{path}"{attributes}/>',
                path=library["url"],
                attributes=flatatt(attributes),
            )
        )

    return format_html_join("\n", "{}", [(stylesheet,) for stylesheet in stylesheets])
