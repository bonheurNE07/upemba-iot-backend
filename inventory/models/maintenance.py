from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from .equipment import Equipment


class MaintenanceLog(models.Model):
    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        related_name="maintenance_logs",
        verbose_name=_("Equipment"),
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="maintenance_logs",
        verbose_name=_("Author"),
    )
    description = models.TextField(_("Description of Issue/Observation"))
    action_taken = models.TextField(
        _("Action Taken"),
        blank=True,
        help_text=_("Actions performed to resolve the issue (if any)"),
    )
    timestamp = models.DateTimeField(_("Timestamp"), auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = _("Maintenance Log")
        verbose_name_plural = _("Maintenance Logs")
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.equipment.name} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
