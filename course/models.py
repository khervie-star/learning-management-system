from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from course.utils import slug_generator

USER = settings.AUTH_USER_MODEL


class Category(models.Model):
    categories = [
        ('Programming and Development', 'Programming and Development'), ('Business',
                                                                         'Business'), ('Finanance and Accounting', 'Finanance and Accounting'),
        ('Personal Development', 'Personal Development'), ('Design', 'Design'), ('Lifestyle',
                                                                                 'Lifestyle'), ('Photography and Video', 'Photography and Video'),
        ('Music', 'Music'), ('Health and Fitness', 'Health and Fitness'), ('Marketing', 'Marketing')
    ]
    name = models.CharField(max_length=100, choices=categories, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Course(models.Model):

    TYPE = [
        ('F', 'Free'), ('P', 'Paid')
    ]

    difficulty = (('Beginner', 'Beginner'), ('Intermediate',
                                             'Intermediate'), ('Advance', 'Advance'))

    author = models.ForeignKey(USER, on_delete=models.PROTECT, related_name='created_courses')
    # remove null = True
    categories = models.ManyToManyField(
        Category, related_name="course_categories")
    name = models.CharField(max_length=500)
    prerequisites = models.TextField()
    duration = models.TextField(help_text='for example 4 months to complete')
    skills_covered = models.TextField()
    level = models.CharField(max_length=15, choices=difficulty)
    course_description = models.TextField()
    # not meant to be nullable. change it
    thumbnail = models.ImageField(upload_to='thumbnail/course/', null=True, blank=True)
    syllabus = models.FileField(upload_to='syllabus/', null=True, blank=True)
    enrolled_students = models.ManyToManyField(USER, blank=True)
    type = models.CharField(max_length=20, choices=TYPE)
    price = models.PositiveIntegerField(help_text=("In Naira"), null=True, blank=True)
    slug = models.SlugField(blank=True, max_length=300, unique=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name

    def total_enrolled_students(self):
        pass

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slug_generator(self)
        return super(Course, self).save(*args, **kwargs)


"""
Remeber to deal with paystack's minumum payment i.e * 100
"""


class Lesson(models.Model):
    name = models.CharField(max_length=1000)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_lessons')
    thumbnail = models.ImageField(upload_to='thumbnail/lesson/')
    descrption = models.CharField(max_length=900)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True, max_length=300, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slug_generator(self)
        return super(Lesson, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class CourseContent(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson_content')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={
        "model__in": ("course", "lesson", "textcontent", "VideoContent")
    })
    target_id = models.PositiveIntegerField()
    target = GenericForeignKey('content_type', 'target_id')


class VideoContent(models.Model):
    url = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='video-content/', blank=True, null=True)


class TextContent(models.Model):
    content = models.TextField()
