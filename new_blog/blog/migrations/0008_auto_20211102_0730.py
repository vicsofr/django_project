# Generated by Django 3.2.8 on 2021-11-02 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_comment_is_child'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(verbose_name='Комментарий'),
        ),
    ]