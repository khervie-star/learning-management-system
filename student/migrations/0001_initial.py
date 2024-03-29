# Generated by Django 3.2.6 on 2021-09-13 13:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0002_coursecontent_lesson_textcontent_videocontent'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avater', models.ImageField(upload_to='student/avatar/')),
                ('firstname', models.CharField(max_length=500)),
                ('lastname', models.CharField(max_length=500)),
                ('email', models.EmailField(max_length=254)),
                ('linkedin', models.CharField(blank=True, max_length=1000, null=True)),
                ('github', models.CharField(blank=True, max_length=2000, null=True)),
                ('courses', models.ManyToManyField(to='course.Course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
