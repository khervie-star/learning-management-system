# Generated by Django 3.2.6 on 2021-09-12 20:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('instructor', '0001_initial'),
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallet',
            name='account_number',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='wallet',
            name='balance',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='wallet',
            name='wallet_owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='my_wallet', to='instructor.instructor'),
        ),
    ]
