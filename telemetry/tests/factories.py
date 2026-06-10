import factory
from factory.django import DjangoModelFactory

from inventory.tests.factories import EquipmentFactory
from telemetry.models import HealthStatus
from telemetry.models import SensorReading


class SensorReadingFactory(DjangoModelFactory[SensorReading]):
    equipment = factory.SubFactory(EquipmentFactory)
    temperature = factory.Faker("pyfloat", min_value=10.0, max_value=80.0)
    voltage = factory.Faker("pyfloat", min_value=200.0, max_value=240.0)
    vib_x = factory.Faker("pyfloat", min_value=0.0, max_value=5.0)
    vib_y = factory.Faker("pyfloat", min_value=0.0, max_value=5.0)
    vib_z = factory.Faker("pyfloat", min_value=0.0, max_value=5.0)

    class Meta:
        model = SensorReading


class HealthStatusFactory(DjangoModelFactory[HealthStatus]):
    equipment = factory.SubFactory(EquipmentFactory)
    status = factory.Iterator(
        [
            HealthStatus.Status.NORMAL,
            HealthStatus.Status.WARNING,
            HealthStatus.Status.CRITICAL,
        ],
    )
    anomaly_score = factory.Faker("pyfloat", min_value=-0.5, max_value=1.5)

    class Meta:
        model = HealthStatus
