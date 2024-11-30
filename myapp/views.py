from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from .models import Channel
from .serializers import ChannelSerializer

def health_check(request):
    return JsonResponse({"message": "Health Check"})

class BaseAPIView(APIView):
    renderer_classes = [JSONRenderer]

class ChannelListView(BaseAPIView):
    def get(self, request):
        channels = Channel.objects.filter(parent_channel__isnull=True)
        serializer = ChannelSerializer(channels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)