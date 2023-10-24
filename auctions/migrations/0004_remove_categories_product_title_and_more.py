# Generated by Django 4.2.4 on 2023-10-23 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_bid_default_bid_alter_bid_last_bid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categories',
            name='product_title',
        ),
        migrations.RemoveField(
            model_name='watchlist',
            name='product_title',
        ),
        migrations.AddField(
            model_name='categories',
            name='product_title',
            field=models.ManyToManyField(blank=True, to='auctions.list_items'),
        ),
        migrations.AddField(
            model_name='watchlist',
            name='product_title',
            field=models.ManyToManyField(blank=True, to='auctions.list_items'),
        ),
    ]