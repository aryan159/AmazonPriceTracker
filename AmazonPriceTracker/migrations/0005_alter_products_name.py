# Generated by Django 3.2.9 on 2021-12-11 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AmazonPriceTracker', '0004_products_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='name',
            field=models.CharField(default='Not Defined', max_length=1000),
        ),
    ]
