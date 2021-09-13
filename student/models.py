from django.db import models
from django.contrib.auth import get_user_model

from course.models import Course

User = get_user_model()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_profile")
    avater = models.ImageField(upload_to='student/avatar/')
    firstname = models.CharField(max_length=500)
    lastname = models.CharField(max_length=500)
    email = models.EmailField()
    linkedin = models.CharField(max_length=1000, blank=True, null=True)
    github = models.CharField(max_length=2000, blank=True, null=True)
    courses = models.ManyToManyField(Course)

    def __str__(self):
        return self.user.name
