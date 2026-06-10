from django.contrib import admin

from .models.health import HealthStatus
from .models.reading import SensorReading


@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    list_display = [
        "equipment",
        "timestamp",
        "temperature",
        "voltage",
        "vib_x",
    ]
    list_filter = ["equipment", "timestamp"]
    search_fields = ["equipment__name"]
    readonly_fields = ["timestamp"]


@admin.register(HealthStatus)
class HealthStatusAdmin(admin.ModelAdmin):
    list_display = ["equipment", "prediction_timestamp", "status", "anomaly_score"]
    list_filter = ["status", "equipment"]
    search_fields = ["equipment__name"]
    readonly_fields = ["prediction_timestamp"]
