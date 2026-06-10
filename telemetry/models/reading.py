from django.db import models
from django.utils.translation import gettext_lazy as _

from inventory.models import Equipment


class SensorReading(models.Model):
    """
    This is the database table that stores every single raw data point sent from the ESP32.
    It acts as the historical log for our sensors.
    """
    
    # This links the reading to the specific hardware node that sent it.
    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        related_name="readings",
        db_index=True, # Makes filtering by equipment much faster
    )

    # --- Sensor Values ---
    temperature = models.FloatField(_("Temperature (°C)"))
    voltage = models.FloatField(_("Voltage (Vrms)"))

    # --- Vibration Data ---
    # The MPU6050 sensor provides 3-axis acceleration data
    vib_x = models.FloatField(_("Vibration X (G)"))
    vib_y = models.FloatField(_("Vibration Y (G)"))
    vib_z = models.FloatField(_("Vibration Z (G)"))

    # Automatically records exactly when this data arrived at our server.
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = _("Sensor Reading")
        verbose_name_plural = _("Sensor Readings")
        # Ensure that by default, queries return the most recent readings first.
        ordering = ["-timestamp"]

    def __str__(self):
        # How this object appears in the Django Admin panel
        return f"{self.equipment.name} @ {self.timestamp}"
