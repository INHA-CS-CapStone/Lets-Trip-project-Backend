from rest_framework import viewsets
from rest_framework.response import Response
from .models import Place
from .models import UserChoice
from .serializers import PlaceSerializer
from .api import api

class PlaceViewSet(viewsets.ViewSet):
    serializer_class = PlaceSerializer

    def list(self, request, *args, **kwargs):
        x = request.query_params.get('x')
        y = request.query_params.get('y')
        df = api(x, y)

        queryset = []
        for name in df['name']:
            place = Place.objects.values('name', 'rating', 'review_count', 'type').get(name=name)
            queryset.append(place)
    
        serializer = PlaceSerializer(queryset, many=True)

        return Response(serializer.data)

class SelectionViewSet(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        data = request.data
        user_choice, created = UserChoice.objects.update_or_create(
            id=1, 
            defaults={'tourism_types': data['tourismTypes'], 'tag_names': data['tagNames']},
        )
        return Response({'status': 'OK'})