# Generated by Django 3.2.6 on 2021-09-13 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0008_auto_20210913_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='transaction_ref',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]