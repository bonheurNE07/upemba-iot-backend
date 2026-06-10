from inventory.models import Equipment
from telemetry.models import HealthStatus
from telemetry.models import SensorReading
from telemetry.services.alert_service import AlertService
from telemetry.services.ml_service import AnomalyDetector


def evaluate_equipment_health_task():
    equipments = Equipment.objects.filter(is_active=True)
    detector = AnomalyDetector(contamination=0.05, n_estimators=15)

    for eq in equipments:
        # Fetch the most recent 100 readings (ordered chronologically oldest to newest for the model)
        recent_qs = SensorReading.objects.filter(equipment=eq).order_by("-timestamp")[
            :40
        ]
        # Query evaluation & reverse for chronological order
        recent_list = list(recent_qs.values(*detector.features, "timestamp"))[::-1]

        if len(recent_list) < 40:
            # We don't have enough data to make an ML prediction yet
            continue

        score, is_anomaly = detector.train_and_predict(recent_list)

        # Map the Isolation Forest score to standard Health Statuses
        # Highly negative is CRITICAL, moderately negative is WARNING, positive is NORMAL
        if score < -0.15:
            status = HealthStatus.Status.CRITICAL
            latest_timestamp = recent_list[-1]["timestamp"]
            # Trigger our Alert Service immediately to warn Park Rangers!
            AlertService.trigger_critical_alert(eq.name, score, latest_timestamp)
        elif is_anomaly or score < 0.0:
            status = HealthStatus.Status.WARNING
        else:
            status = HealthStatus.Status.NORMAL

        HealthStatus.objects.create(equipment=eq, anomaly_score=score, status=status)

    return f"Evaluated health for {equipments.count()} active equipment."
