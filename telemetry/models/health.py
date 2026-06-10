from django.db import models
from django.utils.translation import gettext_lazy as _

from inventory.models import Equipment


class HealthStatus(models.Model):
    class Status(models.TextChoices):
        NORMAL = "NORMAL", _("Normal")
        WARNING = "WARNING", _("Warning")
        CRITICAL = "CRITICAL", _("Critical")

    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        related_name="health_assessments",
    )

    # The raw output from Scikit-Learn Isolation Forest
    # Usually, -1 is an anomaly, 1 is normal
    anomaly_score = models.FloatField(_("Anomaly Score"))

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.NORMAL,
        db_index=True,
    )

    prediction_timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Health Status")
        verbose_name_plural = _("Health Statuses")
        ordering = ["-prediction_timestamp"]

    def __str__(self):
        return f"{self.equipment.name} - {self.status}"
