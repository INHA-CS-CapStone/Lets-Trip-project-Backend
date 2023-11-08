from rest_framework import viewsets
from rest_framework.response import Response
from .models import Place
from .serializers import PlaceSerializer
from .api import api

class PlaceViewSet(viewsets.ViewSet):
    serializer_class = PlaceSerializer

    def list(self, request, *args, **kwargs):
        x = request.query_params.get('x')
        y = request.query_params.get('y')
        df = api(x, y)

        queryset = Place.objects.filter(name__in=df['name']).values('name', 'rating', 'review_count')
        serializer = PlaceSerializer(queryset, many=True)
        
        return Response(serializer.data)
