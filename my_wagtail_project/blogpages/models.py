from django.db import models
from django.core.exceptions import ValidationError

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.images import get_image_model


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

    def get_context(self, request):
        context = super().get_context(request)
        context["blogpages"] = BlogDetail.objects.live().public()
        return context


class BlogDetail(Page):
    # A detail page for a single blog post

    template = "blogpages/blog_detail_page.html"

    parent_page_types = ["blogpages.BlogIndex"]
    subpage_types = []

    image = models.ForeignKey(
        get_image_model(),  # 'wagtailimages.Image' can be used as a string
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    subtitle = models.CharField(max_length=100, blank=True)
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("body"),
        FieldPanel("image"),
    ]

    def clean(self):
        super().clean()

        errors = {}

        # if self.external_link and self.internal_link:
        #     errors['external_cta'] = "Can't have both an external and internal link."
        #     errors['internal_cta'] = "Can't have both an external and internal link."

        if "blog" in self.title.lower():
            errors["title"] = ValidationError(
                "The title must not contain the word 'blog'."
            )

        if "blog" in self.subtitle.lower():
            errors["subtitle"] = ValidationError(
                "The subtitle must not contain the word 'blog'."
            )

        if "blog" in self.slug.lower():
            errors["slug"] = ValidationError(
                "The slug must not contain the word 'blog'."
            )

        if errors:
            raise ValidationError(errors)
