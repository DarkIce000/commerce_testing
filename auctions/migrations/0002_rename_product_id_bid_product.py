# Generated by Django 5.0 on 2023-12-26 13:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bid',
            old_name='product_id',
            new_name='product',
        ),
    ]
