# 1. import stuff
# 2. create a snippet view set
# 3. add some settings for that snippet viewset
# 4. register the class as a snippet

from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import (
    register_snippet,
)  # allows us to register a class as a snippet
from wagtail.snippets.views.snippets import (
    SnippetViewSet,
)  # allows us to create a snippet viewset
from taggit.models import Tag  # import class


@register_snippet
# snippet viewset is a class
class TagSnippetViewSet(SnippetViewSet):
    model = Tag
    icon = "tag"
    add_to_admin_menu = True
    menu_label = "Tags"
    menu_order = 200  # puts in third place
    list_display = ["name", "slug"]
    search_fields = [
        "name",
    ]
    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]
