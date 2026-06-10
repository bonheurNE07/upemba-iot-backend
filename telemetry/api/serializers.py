from rest_framework import serializers

from telemetry.models import HealthStatus
from telemetry.models import SensorReading


class HealthStatusSerializer(serializers.ModelSerializer):
    equipment_name = serializers.CharField(source="equipment.name", read_only=True)

    class Meta:
        model = HealthStatus
        fields = [
            "id",
            "equipment",
            "equipment_name",
            "anomaly_score",
            "status",
            "prediction_timestamp",
        ]
        read_only_fields = ["id", "prediction_timestamp", "equipment_name"]


class SensorReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorReading
        fields = [
            "id",
            "equipment",
            "temperature",
            "voltage",
            "vib_x",
            "vib_y",
            "vib_z",
            "timestamp",
        ]
        read_only_fields = ["id", "timestamp"]
