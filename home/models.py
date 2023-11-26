from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Place(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    keyword = models.CharField(max_length=100, blank=True, null=True)
    rating = models.FloatField(validators=[MinValueValidator(
        0.5), MaxValueValidator(5)], blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    review_count = models.IntegerField(blank=True, null=True)
    x = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True) 
    y = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    content_id = models.IntegerField(blank=True, null=True)
    small_image = models.CharField(max_length=500, null=True, blank=True)


class UserChoice(models.Model):
    tourism_types = models.JSONField()
    tag_names = models.JSONField()

class Planner(models.Model):
    items = models.JSONField()