from django.contrib import admin

from .models import Equipment
from .models import MaintenanceLog


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ["name", "equipment_type", "mac_address", "is_active", "created_at"]
    list_filter = ["equipment_type", "is_active"]
    search_fields = ["name", "mac_address"]


@admin.register(MaintenanceLog)
class MaintenanceLogAdmin(admin.ModelAdmin):
    list_display = ["equipment", "author", "timestamp"]
    list_filter = ["timestamp", "author"]
    search_fields = ["equipment__name", "description", "action_taken"]
