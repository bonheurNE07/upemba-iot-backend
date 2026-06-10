import pytest
from django.core import mail

from telemetry.services.alert_service import AlertService
from telemetry.services.ml_service import AnomalyDetector
from users.models import User


@pytest.mark.django_db
def test_alert_service_dispatch(user, settings):
    settings.EMAIL_HOST_USER = "mock"
    settings.EMAIL_HOST_PASSWORD = "mock"  # noqa: S105
    user.role = User.Role.TECHNICIAN
    user.save()

    AlertService.trigger_critical_alert(
        "Solar Inverter 1",
        -0.99,
        "2025-01-01 12:00:00",
    )

    # Assert one message has been correctly sent to the Django testing outbox sandbox
    assert len(mail.outbox) == 1
    assert "Solar Inverter 1" in mail.outbox[0].subject
    assert user.email in mail.outbox[0].to


def test_anomaly_detector_insufficient_data():
    detector = AnomalyDetector()
    score, is_anomaly = detector.train_and_predict([])

    # Should safely fallback instead of throwing Math exceptions
    assert score == 1.0
    assert not is_anomaly
