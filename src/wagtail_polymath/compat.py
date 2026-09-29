from django import VERSION as DJANGO_VERSION


if DJANGO_VERSION >= (6, 1):
    from django.forms import Stylesheet as DjangoStylesheet

    class Stylesheet(DjangoStylesheet): ...
else:
    from django.forms.widgets import MediaAsset

    class Stylesheet(MediaAsset):
        element_template = '<link href="{path}"{attributes}>'

        def __init__(self, href, media: str | None = "all", **attributes):
            super().__init__(path=href, rel="stylesheet", media=media, **attributes)
