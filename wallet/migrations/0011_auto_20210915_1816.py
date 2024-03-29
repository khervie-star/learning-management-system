# Generated by Django 3.2.6 on 2021-09-15 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0010_auto_20210915_1745'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transfers',
            options={'verbose_name_plural': 'Transfers'},
        ),
        migrations.RenameField(
            model_name='transfers',
            old_name='aaccount_number',
            new_name='account_number',
        ),
        migrations.AddField(
            model_name='transfers',
            name='account_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='transfers',
            name='amount',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='transfers',
            name='bank_name',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='transfers',
            name='tranferred',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='transfers',
            name='transfer_reference',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
