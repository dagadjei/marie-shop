# Generated by Django 3.1.1 on 2020-09-23 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_item_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
