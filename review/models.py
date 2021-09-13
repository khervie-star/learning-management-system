from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.utils import timezone

from course.models import Course

User = get_user_model()


class Rating(models.Model):
    rated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="ratings")
    count = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(5)], null=True)
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def average_rating():
        pass
