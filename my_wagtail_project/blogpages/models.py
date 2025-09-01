from django.db import models
from django.core.exceptions import ValidationError

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.admin.panels import FieldPanel
from wagtail.blocks import TextBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail import blocks
from wagtail.fields import RichTextField
from wagtail.fields import StreamField
from wagtail.images import get_image_model
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from wagtail.snippets.blocks import SnippetChooserBlock

from blocks import blocks as custom_blocks


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


class BlogDetailTag(TaggedItemBase):
    content_object = ParentalKey(
        "blogpages.BlogDetail",
        related_name="tagged_items",
        on_delete=models.CASCADE,
    )


class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()  # Could make this a rich text field

    def __str__(self):
        return self.name


class BlogDetail(Page):  # Django model not Wagtail page
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
    body = RichTextField(
        blank=True, features=["blockquote", "code", "image", "strikethrough"]
    )

    body_as_streamfield = StreamField(
        [
            ("info", custom_blocks.InfoBlock()),
            ("faq", custom_blocks.FAQListBlock()),
            ("image", custom_blocks.ImageBlock()),
            ("document", DocumentChooserBlock(group="Standalone Blocks")),
            (
                "page",
                blocks.PageChooserBlock(
                    group="Standalone Blocks", page_type="home.homePage", required=False
                ),
            ),
            ("author", SnippetChooserBlock("blogpages.Author")),
            (
                "text",
                custom_blocks.TextBlock(),
            ),
            (
                "carousel",
                custom_blocks.CarouselBlock(),
            ),
            (
                "call_to_action_1",
                custom_blocks.CallToAction1Block(),
            ),
        ],
        block_counts={
            # "text": {"min_num": 1, "max_num": 10},
            "image": {"min_num": 0, "max_num": 1},
        },
        use_json_field=True,  # Is this still correct synatx in Wagtail 6?
        blank=True,  # For when we save the page
        null=True,  # A field that has no info in, not prepopulated
    )

    tags = ClusterTaggableManager(through=BlogDetailTag, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("tags"),
        FieldPanel("subtitle"),
        FieldPanel("body"),
        FieldPanel("body_as_streamfield"),
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
