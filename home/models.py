from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Place(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    keyword = models.CharField(max_length=100, blank=True, null=True)
    rating = models.FloatField(validators=[MinValueValidator(
        0.5), MaxValueValidator(5)], blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    review_count = models.IntegerField(blank=True, null=True)

class UserChoice(models.Model):
    tourism_types = models.JSONField()
    tag_names = models.JSONField()