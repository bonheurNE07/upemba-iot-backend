import pytest

from inventory.models import Equipment
from inventory.models import MaintenanceLog


@pytest.mark.django_db
def test_equipment_str(equipment: Equipment):
    assert str(equipment) == f"{equipment.name} ({equipment.mac_address})"


@pytest.mark.django_db
def test_maintenance_log_str(maintenance_log: MaintenanceLog):
    expected = f"{maintenance_log.equipment.name} - {maintenance_log.timestamp.strftime('%Y-%m-%d %H:%M')}"
    assert str(maintenance_log) == expected
