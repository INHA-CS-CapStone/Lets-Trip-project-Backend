from rest_framework import serializers
from .models import Place, Planner

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['name', 'rating', 'x', 'y', 'content_id', 'small_image']

class PlannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planner
        fields = ['id', 'items']