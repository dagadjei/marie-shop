# Generated by Django 3.1.1 on 2020-09-23 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20200923_1845'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='slug',
            field=models.SlugField(default='test product'),
            preserve_default=False,
        ),
    ]