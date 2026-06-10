import pytest


@pytest.mark.django_db
class TestTelemetryAPIViews:
    def test_sensors_readonly(self, admin_client, sensor_reading):
        response = admin_client.get("/api/sensor-readings/")
        assert response.status_code == 200

        # Telemetry ingestion endpoints should strictly be internal services over MQTT
        # HTTP POSTs must be explicitly blocked
        post_response = admin_client.post("/api/sensor-readings/", {})
        assert post_response.status_code == 405

    def test_health_readonly(self, admin_client, health_status):
        response = admin_client.get("/api/health-status/")
        assert response.status_code == 200

        post_response = admin_client.post("/api/health-status/", {})
        assert post_response.status_code == 405
