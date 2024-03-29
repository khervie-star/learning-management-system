# Generated by Django 3.2.6 on 2021-09-13 13:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
        ('wallet', '0007_alter_payment_course_to_enroll'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='auth_student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student.profile'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
