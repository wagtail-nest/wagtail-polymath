from django import template
from django.forms import Script
from wagtail.admin.staticfiles import versioned_static


register = template.Library()


@register.simple_tag
def mathjax_script():
    init_script = Script(versioned_static("wagtail_polymath/js/mathjax_init.js"))
    library = Script(
        versioned_static("wagtail_polymath/js/vendor/mathjax/tex-mml-chtml.js"),
        defer=True,
    )

    return str(init_script) + str(library)
