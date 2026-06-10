import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Equipment(models.Model):
    class Type(models.TextChoices):
        INVERTER = "INVERTER", _("Solar Inverter")
        MOTOR = "MOTOR", _("Motor/Pump")
        SERVER = "SERVER", _("Server Room")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=255,
        help_text=_("Human-readable name of the equipment"),
    )
    equipment_type = models.CharField(
        max_length=20,
        choices=Type.choices,
        default=Type.INVERTER,
    )
    mac_address = models.CharField(
        max_length=100,
        unique=True,
        help_text=_("Unique identifier from the ESP32"),
    )
    location_notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Equipment")
        verbose_name_plural = _("Equipments")

    def __str__(self):
        return f"{self.name} ({self.mac_address})"
