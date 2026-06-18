from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from wagtail_polymath.blocks import MathBlock


class MathPage(Page):
    body = StreamField(
        [
            ("heading", blocks.CharBlock(classname="full title")),
            ("paragraph", blocks.RichTextBlock()),
            ("equation", MathBlock()),
        ],
        use_json_field=True,
    )

    content_panels = Page.content_panels + [FieldPanel("body")]
