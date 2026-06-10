import pytest

from telemetry.models import HealthStatus
from telemetry.models import SensorReading


@pytest.mark.django_db
def test_sensor_reading_str(sensor_reading: SensorReading):
    expected = f"{sensor_reading.equipment.name} @ {sensor_reading.timestamp}"
    assert str(sensor_reading) == expected


@pytest.mark.django_db
def test_health_status_str(health_status: HealthStatus):
    expected = f"{health_status.equipment.name} - {health_status.status}"
    assert str(health_status) == expected
