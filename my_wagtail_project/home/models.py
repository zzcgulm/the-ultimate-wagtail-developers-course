from django.db import models
from django.core.exceptions import ValidationError

from modelcluster.fields import ParentalKey

from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    HelpPanel,
    InlinePanel,
    MultiFieldPanel,
    MultipleChooserPanel,
    PageChooserPanel,
    TitleFieldPanel,
)
from wagtail.documents import get_document_model
from wagtail.fields import RichTextField
from wagtail.images import get_image_model
from wagtail.models import Orderable, Page


class GalleryImage(Orderable):
    page = ParentalKey(
        "home.HomePage", on_delete=models.CASCADE, related_name="gallery_images"
    )
    image = models.ForeignKey(
        get_image_model(),
        blank=False,
        on_delete=models.CASCADE,
        null=False,
        related_name="+",
    )
    panels = [
        FieldPanel("image"),
    ]


class HomePage(Page):

    template = "home/home_page.html"

    max_count = 1

    subtitle = models.CharField(max_length=100, blank=True, null=True)

    body = RichTextField(blank=True)

    image = models.ForeignKey(
        get_image_model(),  # 'wagtailimages.Image' can be used as a string
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    custom_document = models.ForeignKey(
        get_document_model(),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    cta_url = models.ForeignKey(
        "blogpages.BlogIndex",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",  # Don't really need this
    )

    cta_external_url = models.URLField(blank=True, null=True)

    content_panels = Page.content_panels + [
        TitleFieldPanel(
            "subtitle",
            help_text="The subtitle will appear below the title",
            placeholder="Enter your subtitle here",
        ),  # For Title field
        HelpPanel(
            content="<strong>Help Panel</strong><p>Help text goes here.</p>",
            heading="Note:",
        ),
        FieldRowPanel(  # Places fields side by side
            [
                PageChooserPanel(
                    "cta_url",
                    "blogpages.BlogDetail",  # Limit to specific page type
                    classname="col4",
                    heading="Blog Page Selection",
                    help_text="Select the appropriate blog page.",
                ),
                FieldPanel(
                    "cta_external_url",
                    classname="col8",
                    heading="External URL",
                    help_text="Enter the external URL.",
                ),
            ],
            heading="Call to Action URLs",
            help_text="Select a page or enter a URL",
        ),
        MultiFieldPanel(
            [
                FieldPanel("subtitle"),
            ],
            classname="collapsed",  # Makes it collapsed by default
            heading="MultiFieldPanel Demo",
            help_text="Random help text",
        ),
        InlinePanel("gallery_images", label="Gallery Images", max_num=4, min_num=2),
        MultipleChooserPanel(  # Can choose multiple images in one go using this
            "gallery_images",
            chooser_field_name="image",
            icon="image",
            label="Gallery Images",
            max_num=4,
            min_num=2,
        ),
        # FieldPanel("subtitle", read_only=True),
        # FieldPanel("cta_url"),
        # FieldPanel("cta_external_url"),
        # FieldPanel("body"),
        # FieldPanel("image"),
        # FieldPanel("custom_document"),
    ]

    @property
    def get_cta_url(self):
        if self.cta_url:
            return self.cta_url.url
        elif self.cta_external_url:
            return self.cta_external_url
        else:
            return None

    def clean(self):
        super().clean()

        errors = {}

        if self.cta_url and self.cta_external_url:
            raise ValidationError(
                {
                    "cta_url": "Can't have both an external and internal CTA link.",
                    "cta_external_url": "Can't have both an external and internal CTA link.",
                }
            )
