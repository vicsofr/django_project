# Generated by Django 3.2.8 on 2021-11-01 12:19

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_posts_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Содержание'),
        ),
    ]
