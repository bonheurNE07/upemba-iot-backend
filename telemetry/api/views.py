from rest_framework import viewsets

from telemetry.models import HealthStatus
from telemetry.models import SensorReading

from .serializers import HealthStatusSerializer
from .serializers import SensorReadingSerializer


class HealthStatusViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This class handles the API endpoint that the Next.js Frontend calls to get Health Statuses.
    It is 'ReadOnly' because the frontend is never allowed to CREATE a health status.
    Health statuses are only created automatically by our Machine Learning background task.
    """
    
    # By default, we grab all health statuses and order them so the newest predictions are first.
    queryset = HealthStatus.objects.all().order_by("-prediction_timestamp")
    
    # The Serializer translates our Python database objects into JSON format for the frontend.
    serializer_class = HealthStatusSerializer

    def get_queryset(self):
        """
        This function allows the frontend to 'filter' the data it requests.
        Instead of downloading thousands of statuses, the frontend can ask for specific ones.
        """
        # Start with the default list of all statuses
        queryset = super().get_queryset()
        
        # Check if the frontend added any filter parameters to the URL 
        # e.g., /api/health-status/?equipment=EQUIP-INV-001
        equipment = self.request.query_params.get("equipment")
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")

        # If the frontend asked for a specific equipment, we filter the list to only include that equipment
        if equipment:
            queryset = queryset.filter(equipment_id=equipment)
            
        # If the frontend asked for data AFTER a certain date
        if start_date:
            queryset = queryset.filter(prediction_timestamp__gte=start_date)
            
        # If the frontend asked for data BEFORE a certain date
        if end_date:
            queryset = queryset.filter(prediction_timestamp__lte=end_date)
            
        # Return the final, filtered list of statuses back to the frontend
        return queryset

class SensorReadingViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This class handles the API endpoint for raw Sensor Readings (Temperature, Voltage, etc).
    It is also 'ReadOnly' because sensor data only comes from the ESP32 via MQTT, never from the frontend.
    """
    queryset = SensorReading.objects.all()
    serializer_class = SensorReadingSerializer
