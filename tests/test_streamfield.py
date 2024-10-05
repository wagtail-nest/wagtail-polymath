from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from testapp.models import MathPage
from wagtail.blocks.stream_block import StreamValue
from wagtail.models import Page
from wagtail.test.utils import WagtailTestUtils


class TestStreamField(WagtailTestUtils, TestCase):
    def setUp(self):
        self.user = self.login()

        # Convert the user into an moderator
        self.moderators_group = Group.objects.get(name="Moderators")
        for permission in Permission.objects.filter(
            content_type=ContentType.objects.get_for_model(MathPage)
        ):
            self.moderators_group.permissions.add(permission)
        self.user.is_superuser = False
        self.user.groups.add(self.moderators_group)
        self.user.save()

        # Create test page with a draft revision
        self.page = Page.objects.get(id=1).add_child(
            instance=MathPage(title="Test", slug="test")
        )

        self.page.body = StreamValue(
            stream_block=self.page.body.stream_block,
            stream_data=[
                {
                    "type": "equation",
                    "value": "$ y = ax + b $",
                }
            ],
            is_lazy=True,
        )

        self.page.save_revision().publish()

    def test_streamfield_value(self):
        page = MathPage.objects.first()
        self.assertTrue(page is not None)

        response = self.client.get(f"/admin/pages/{page.id}/edit/")
        self.assertEqual(response.status_code, 200)

        self.assertRegex(
            response.content.decode(),
            r"&quot;value&quot;: &quot;\$ y = ax \+ b \$&quot;",
        )
