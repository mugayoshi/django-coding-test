from django.urls import path
from .views import ChannelListView, health_check 

urlpatterns = [
   path('api/health/', health_check, name='health check'),
   path('api/channels/', ChannelListView.as_view(), name='channel list')
]