# Generated by Django 3.2.6 on 2021-09-17 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0013_auto_20210917_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionlog',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='transactionlog',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
