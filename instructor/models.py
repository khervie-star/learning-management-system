from django.db import models
from django.contrib.auth import get_user_model

USER = get_user_model()


class Instructor(models.Model):
    instructor = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="instructor")
    avatar = models.ImageField(upload_to='instructor/avatar/', null=True, blank=True)
    firstname = models.CharField(max_length=600)
    lastname = models.CharField(max_length=600)
    linkedin = models.CharField(max_length=1000, blank=True, null=True)
    github = models.CharField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return self.firstname + ' ' + self.lastname
