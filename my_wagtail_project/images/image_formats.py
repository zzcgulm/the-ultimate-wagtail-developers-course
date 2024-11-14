from wagtail.images.formats import (
    Format,
    register_image_format,
)

register_image_format(
    Format("left-aligned", "Left-aligned", "richtext-image left-aligned", "width-150")
)

register_image_format(Format("x", "X", "xx", "width-150"))
