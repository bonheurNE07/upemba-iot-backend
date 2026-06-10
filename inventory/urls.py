from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.views import EquipmentViewSet, MaintenanceLogViewSet

router = DefaultRouter()
router.register(r'equipment', EquipmentViewSet, basename='equipment')
router.register(r'maintenance-logs', MaintenanceLogViewSet, basename='maintenance-log')

urlpatterns = [
    path('', include(router.urls)),
]
