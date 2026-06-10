from django.db import models
from django.utils.translation import gettext_lazy as _

from inventory.models import Equipment


class SensorReading(models.Model):
    # We use a string reference "inventory.Equipment" to avoid circular imports
    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        related_name="readings",
        db_index=True,
    )

    # Sensor Values
    temperature = models.FloatField(_("Temperature (°C)"))
    voltage = models.FloatField(_("Voltage (Vrms)"))

    # Vibration Axis
    vib_x = models.FloatField(_("Vibration X (G)"))
    vib_y = models.FloatField(_("Vibration Y (G)"))
    vib_z = models.FloatField(_("Vibration Z (G)"))

    # Meta
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = _("Sensor Reading")
        verbose_name_plural = _("Sensor Readings")
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.equipment.name} @ {self.timestamp}"
