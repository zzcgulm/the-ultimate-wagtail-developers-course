# Generated by Django 4.2.16 on 2024-09-27 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_homepage_cta_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='cta_external_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]