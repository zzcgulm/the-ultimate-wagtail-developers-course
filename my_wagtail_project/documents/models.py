from django.db import models

# Create your models here.
from wagtail.documents.models import AbstractDocument, Document


class CustomDocument(AbstractDocument):
    document_description = models.CharField(blank=True, max_length=255)

    admin_form_fields = Document.admin_form_fields + ("document_description",)
