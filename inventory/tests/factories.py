import factory
from factory.django import DjangoModelFactory

from inventory.models import Equipment
from inventory.models import MaintenanceLog
from users.tests.factories import UserFactory


class EquipmentFactory(DjangoModelFactory[Equipment]):
    name = factory.Faker("word")
    equipment_type = "SOLAR_INVERTER"
    mac_address = factory.Faker("mac_address")
    is_active = True

    class Meta:
        model = Equipment
        django_get_or_create = ["mac_address"]


class MaintenanceLogFactory(DjangoModelFactory[MaintenanceLog]):
    equipment = factory.SubFactory(EquipmentFactory)
    author = factory.SubFactory(UserFactory)
    description = factory.Faker("sentence")
    action_taken = factory.Faker("paragraph")

    class Meta:
        model = MaintenanceLog
