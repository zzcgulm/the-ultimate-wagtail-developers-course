from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class BlogIndex(Page):
    # A listing page of all child pages

    template = "blogpages/blog_index_page.html"

    max_count = 1
    parent_page_types = ["home.homePage"]
    subpage_types = ["blogpages.BlogDetail"]

    subtitle = models.CharField(max_length=100, blank=True)
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("body"),
    ]


class BlogDetail(Page):
    # A detail page for a single blog post

    template = "blogpages/blog_detail_page.html"

    parent_page_types = ["blogpages.BlogIndex"]

    subtitle = models.CharField(max_length=100, blank=True)
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("body"),
    ]
