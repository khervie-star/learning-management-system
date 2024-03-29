# Generated by Django 3.2.6 on 2021-09-13 13:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Programming and Development', 'Programming and Development'), ('Business', 'Business'), ('Finanance and Accounting', 'Finanance and Accounting'), ('Personal Development', 'Personal Development'), ('Design', 'Design'), ('Lifestyle', 'Lifestyle'), ('Photography and Video', 'Photography and Video'), ('Music', 'Music'), ('Health and Fitness', 'Health and Fitness'), ('Marketing', 'Marketing')], max_length=100, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('prerequisites', models.TextField()),
                ('duration', models.TextField(help_text='for example 4 months to complete')),
                ('skills_covered', models.TextField()),
                ('level', models.CharField(choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advance', 'Advance')], max_length=15)),
                ('course_description', models.TextField()),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='thumbnail/course/')),
                ('syllabus', models.FileField(blank=True, null=True, upload_to='syllabus/')),
                ('type', models.CharField(choices=[('F', 'Free'), ('P', 'Paid')], max_length=20)),
                ('price', models.PositiveIntegerField(blank=True, help_text='In Naira', null=True)),
                ('slug', models.SlugField(blank=True, max_length=300, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_courses', to=settings.AUTH_USER_MODEL)),
                ('categories', models.ManyToManyField(related_name='course_categories', to='course.Category')),
                ('enrolled_students', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
