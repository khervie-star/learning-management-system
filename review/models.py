from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

from instructor.models import Course

User = get_user_model()


class Rating(models.Model):
    rated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="ratings")
    count = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(5)], null=True)

    def average_rating():
        pass
