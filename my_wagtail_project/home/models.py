from django.db import models

from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page


class HomePage(Page):
    # pass

    template = "home/home_page.html"

    subtitle = models.CharField(max_length=100, blank=True, null=True)

    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("subtitle", read_only=True),
        FieldPanel("body"),
    ]
