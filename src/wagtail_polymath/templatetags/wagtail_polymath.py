from typing import TYPE_CHECKING, Any

from django import template
from django.forms.utils import flatatt
from django.utils.html import format_html, format_html_join
from wagtail.admin.staticfiles import versioned_static

from wagtail_polymath.config import wagtail_polymath_config


if TYPE_CHECKING:
    from django.utils.safestring import SafeString

    from wagtail_polymath.config import LibraryDict

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
    if wagtail_polymath_config.init_js:
        init_attributes = {}
        if config_json := wagtail_polymath_config.mathjax_config_json:
            init_attributes["data-polymath-config"] = config_json
        scripts.append(
            format_html(
                '<script src="{init_path}"{attributes}></script>',
                init_path=versioned_static(wagtail_polymath_config.init_js),
                attributes=flatatt(init_attributes),
            )
        )
    for library in wagtail_polymath_config.libraries_js:
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
    for library in wagtail_polymath_config.libraries_css:
        attributes = _build_attributes(library, defer=False)
        stylesheets.append(
            format_html(
                '<link rel="stylesheet" href="{path}"{attributes}/>',
                path=library["url"],
                attributes=flatatt(attributes),
            )
        )

    return format_html_join("\n", "{}", [(stylesheet,) for stylesheet in stylesheets])
