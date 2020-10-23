# Generated by Django 3.1 on 2020-10-18 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuctionProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=30)),
                ('seller', models.CharField(default='Unknown', max_length=30)),
                ('location', models.CharField(default='', max_length=30)),
                ('basePrice', models.FloatField(default=1.0)),
                ('bestPrice', models.FloatField(default=None)),
                ('date', models.DateTimeField()),
                ('whoWon', models.CharField(blank=True, default='', max_length=30)),
                ('jsonResult', models.CharField(blank=True, default='', max_length=500)),
            ],
        ),
    ]