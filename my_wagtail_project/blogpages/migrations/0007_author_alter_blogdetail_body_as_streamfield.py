# Generated by Django 4.2.16 on 2025-01-17 11:21

from django.db import migrations, models
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blogpages', '0006_alter_blogdetail_body_as_streamfield'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('bio', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='blogdetail',
            name='body_as_streamfield',
            field=wagtail.fields.StreamField([('image', 0), ('document', 1), ('page', 2)], blank=True, block_lookup={0: ('wagtail.images.blocks.ImageChooserBlock', (), {}), 1: ('wagtail.documents.blocks.DocumentChooserBlock', (), {}), 2: ('wagtail.blocks.PageChooserBlock', (), {'page_type': ['home.HomePage'], 'required': False})}, null=True),
        ),
    ]
