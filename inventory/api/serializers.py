from rest_framework import serializers

from inventory.models import Equipment
from inventory.models import MaintenanceLog


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = [
            "id",
            "name",
            "equipment_type",
            "mac_address",
            "location_notes",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class MaintenanceLogSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = MaintenanceLog
        fields = [
            "id",
            "equipment",
            "author",
            "author_name",
            "description",
            "action_taken",
            "timestamp",
        ]
        read_only_fields = ["id", "timestamp", "author_name", "author"]
