from django.contrib import admin

from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


# Register your models here.
class TextBlock(blocks.TextBlock):
    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
            help_text="This is from my TextBlock (help text is here)",
            # max_length=200, # example of config that can be used
            # min_length=10, # example of config that can be used
            # required=False # example of config that can be used
        )

    class Meta:
        # template = "..."
        ...


class InfoBlock(blocks.StaticBlock):
    class Meta:
        icon = "..."
        label = "..."
        admin_text = "This is from my InfoBlock"
        label = "General information"


class FAQBlock(blocks.StructBlock):
    question = blocks.CharBlock()
    answer = (
        blocks.RichTextBlock(
            features=["bold", "italic"],
        ),
    )


class FAQListBlock(blocks.ListBlock):
    def __init__(self, **kwargs):
        super().__init__(FAQBlock(), **kwargs)

    class Meta:
        min_num = 1
        max_num = 5
        label = "Frequently Asked Questions 2"
        # icon = "..."
        # template = "..."


class CarouselBlock(blocks.StreamBlock):
    image = ImageChooserBlock()
    quotation = blocks.StructBlock(
        [
            (
                "text",
                blocks.TextBlock(),
            ),  # uses Wagtail TextBlock, not our custom TextBlock
            (
                "author",
                blocks.TextBlock(),
            ),  # uses Wagtail TextBlock, not our custom TextBlock
        ]
    )

    class Meta:
        # min_num = 1
        # max_num = 5
        # label = "Carousel"
        # icon = "image"
        # template = "..."
        ...


class CallToAction1Block(blocks.StructBlock):
    text = blocks.RichTextBlock(features=["link"])
    page = blocks.PageChooserBlock()
    button_text = blocks.CharBlock(max_length=100, required=False)

    class Meta:
        label = "CTA #1"


class ImageBlock(ImageChooserBlock):

    class Meta:
        # template = "...",
        ...
