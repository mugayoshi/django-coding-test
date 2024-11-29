from django.urls import path
from .views import health_check 
urlpatterns = [
   path('api/health/', health_check, name='health check'),
]