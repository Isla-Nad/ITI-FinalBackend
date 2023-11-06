from django.db import models
from accounts.models import User
from django.core.validators import MaxValueValidator


# Create your models here.


class Review(models.Model):
    reviewing_user = models.ForeignKey(
        User, related_name='reviews_given', on_delete=models.CASCADE)
    reviewed_user = models.ForeignKey(
        User, related_name='reviews_received', on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MaxValueValidator(limit_value=5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.reviewing_user.first_name} reviewed {self.reviewed_user.first_name}"
