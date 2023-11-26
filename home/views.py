from rest_framework import viewsets, status
from rest_framework.response import Response
from django.http import JsonResponse
from .models import Place, UserChoice, Planner
from .serializers import PlaceSerializer, PlannerSerializer
from .api import api
from .restaurant import restaurant
from .detail import detail

class PlaceViewSet(viewsets.ViewSet):
    serializer_class = PlaceSerializer

    def list(self, request, *args, **kwargs):
        x = request.query_params.get('x')
        y = request.query_params.get('y')
        df = api(x, y)

        print(df['name'].tolist())
        queryset = []
        for name in df['name']:
            place = Place.objects.values('name', 'rating', 'x', 'y', 'content_id', 'small_image').get(name=name)
            queryset.append(place)
    
        serializer = PlaceSerializer(queryset, many=True)

        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        content_id = pk
        if content_id is not None:
            data = detail(content_id)
            return Response(data) 
        else:
            return Response({'error': 'content_id is required'}, status=status.HTTP_400_BAD_REQUEST)


class SelectionViewSet(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        data = request.data
        user_choice, created = UserChoice.objects.update_or_create(
            id=1, 
            defaults={'tourism_types': data['tourismTypes'], 'tag_names': data['tagNames']},
        )
        return Response({'status': 'OK'})
    
def get_restaurants(request):
    x = request.GET.get('x')
    y = request.GET.get('y')

    if x is None or y is None:
        return JsonResponse({'error': 'Invalid parameters'}, status=400)

    result = restaurant(x, y)
    return JsonResponse({'result': result})

class PlannerViewSet(viewsets.ViewSet):
    queryset = Planner.objects.all()
    serializer_class = PlannerSerializer

    def list(self, request, *args, **kwargs):
        planners = Planner.objects.all()
        if not planners:
            return Response([]) 
        serializer = PlannerSerializer(planners, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data
        items = data.get('items')

        if items is not None:
            planner = Planner(items=items)
            planner.save()
            return Response({'status': 'success', 'id': planner.id}, status=200)
        else:
            return Response({'status': 'error', 'error': 'Invalid data'}, status=400)

    def destroy(self, request, *args, **kwargs):
        try:
            planner = Planner.objects.get(pk=kwargs['pk'])
            planner.delete()
            return Response({'status': 'success'}, status=200)
        except Planner.DoesNotExist:
            return Response({'status': 'error', 'error': 'Planner not found'}, status=400)