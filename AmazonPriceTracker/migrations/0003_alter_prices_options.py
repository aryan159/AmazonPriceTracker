# Generated by Django 3.2.9 on 2021-12-07 07:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AmazonPriceTracker', '0002_auto_20211202_2157'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='prices',
            options={'ordering': ['-date']},
        ),
    ]