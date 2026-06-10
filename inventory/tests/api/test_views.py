import pytest


@pytest.mark.django_db
class TestEquipmentViewSet:
    def test_list_equipment(self, equipment, admin_client):
        response = admin_client.get("/api/equipment/")

        assert response.status_code == 200
        # Since pagination might be enabled by default in Cookiecutter Django DRF
        data = response.data["results"] if "results" in response.data else response.data

        assert len(data) >= 1
        assert data[0]["name"] == equipment.name
        assert data[0]["equipment_type"] == equipment.equipment_type


@pytest.mark.django_db
class TestMaintenanceLogViewSet:
    def test_create_auto_assigns_author(self, user, equipment, client):
        client.force_login(user)

        payload = {
            "equipment": str(equipment.id),
            "description": "Replaced thermal fuse.",
            "action_taken": "The sensor was malfunctioning due to heat.",
        }

        response = client.post("/api/maintenance-logs/", payload)
        assert response.status_code == 201

        # Verify the database explicitly captured the authenticated user despite not being in the payload
        from inventory.models import MaintenanceLog

        log = MaintenanceLog.objects.get(id=response.data["id"])

        assert log.author == user
        assert log.author.username == user.username
        # Assert serializer correctly exposed the read-only author name
        assert response.data["author_name"] == user.username
