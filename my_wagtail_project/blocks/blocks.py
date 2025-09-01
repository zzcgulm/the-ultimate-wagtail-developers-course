from django.contrib import admin
from django.core.exceptions import ValidationError

from wagtail import blocks
from wagtail.blocks import ListBlockValidationError
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

    def clean(self, value):
        value = super().clean(value)
        if "wordpress" in value.lower():
            raise ValidationError("We don't like WordPress here!")
        return value

    class Meta:
        icon = "strikethrough"
        group = "Standalone Blocks"
        template = "blocks/text_block.html"
        ...


class InfoBlock(blocks.StaticBlock):
    class Meta:
        admin_text = "This is from my InfoBlock"
        icon = "..."
        group = "Standalone Blocks"
        label = "General information"
        template = "blocks/info_block.html"


from wagtail.blocks import StructBlockValidationError


class FAQBlock(blocks.StructBlock):
    question = blocks.CharBlock()
    answer = (
        blocks.RichTextBlock(
            features=["bold", "italic"],
        ),
    )

    # def clean(self, value):
    #     cleaned_data = super().clean(value)
    #     if "wordpress" in cleaned_data["question"].lower():
    #         raise StructBlockValidationError(
    #             block_errors_question={
    #                 "question": ValidationError("We don't like WordPress here!")
    #             }
    #         )
    #     return cleaned_data


class FAQListBlock(blocks.ListBlock):
    def __init__(self, **kwargs):
        super().__init__(FAQBlock(), **kwargs)

    def clean(self, value):
        cleaned_data = super().clean(value)
        errors = {}

        for index, obj in enumerate(
            cleaned_data
        ):  # Loop though cleaned_data; `obj` is each FAQBlock
            if "wordpress" in str(obj["question"]).lower():
                errors[index] = ValidationError("We don't like WordPress here!")

        if errors:
            raise ListBlockValidationError(block_errors=errors)

        return cleaned_data

    class Meta:
        group = "Iterables"
        # icon = "..."
        label = "Frequently Asked Questions 2"
        min_num = 1
        max_num = 5
        template = "blocks/faq_list_block.html"


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

    # Business logic to ensure admin UI creates sensible output, eg same number of images as quotations
    def clean(self, value):
        value = super().clean(value)
        images = [item for item in value if item.block_type == "image"]
        quotations = [item for item in value if item.block_type == "quotation"]

        if not images or not quotations:
            raise ValidationError("You need at least one image and one quotation.")

        if len(images) != len(quotations):
            raise ValidationError("You need the same number of images and quotations.")
        return value

    class Meta:
        group = "Iterables"
        # icon = "image"
        # label = "Carousel"
        # min_num = 1
        # max_num = 5
        template = "blocks/carousel_block.html"
        ...


class CallToAction1Block(blocks.StructBlock):
    text = blocks.RichTextBlock(features=["link"])
    page = blocks.PageChooserBlock()
    button_text = blocks.CharBlock(max_length=100, required=False)

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        page = value.get("page")
        button_text = value.get("button_text")
        context["button_copy"] = button_text if button_text else f"Read: {page.title}"
        return context

    class Meta:
        label = "CTA #1"
        template = "blocks/call_to_action_1_block.html"


class ImageBlock(ImageChooserBlock):

    def get_context(self, value, parent_context=None):
        from blogpages.models import (
            BlogDetail,
        )  # Import here rather than at top to avoid circular ImportError

        context = super().get_context(value, parent_context)
        context["blog_posts"] = BlogDetail.objects.live().public()
        return context

    class Meta:
        group = "Standalone Blocks"
        template = "blocks/image_block.html"


class PersonBlock(blocks.StructBlock):
    name = blocks.CharBlock(required=True)
    biography = blocks.RichTextBlock()
    image = ImageChooserBlock()

    # ..
    class Meta:
        icon = "user"
        label = "Person Profile"
        template = "blocks/person_block.html"
