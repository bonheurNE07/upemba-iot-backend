from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.views import HealthStatusViewSet, SensorReadingViewSet

router = DefaultRouter()
router.register(r'health-status', HealthStatusViewSet, basename='health-status')
router.register(r'sensor-readings', SensorReadingViewSet, basename='sensor-readings')

urlpatterns = [
    path('', include(router.urls)),
]
