# Generated by Django 3.1 on 2020-10-23 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0003_auto_20201023_2353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionproduct',
            name='hash',
            field=models.CharField(blank=True, default=None, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='auctionproduct',
            name='txId',
            field=models.CharField(blank=True, default=None, max_length=66, null=True),
        ),
    ]
