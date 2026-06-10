# Telemetry Celery Tasks Documentation

This document explains the asynchronous background processes governing the application.

## `evaluate_equipment_health_task`
File: `backend/telemetry/tasks.py`

This `shared_task` is structurally bound to the Celery Beat scheduler and represents the heartbeat of the predictive maintenance engine.

**Execution Flow:**
1. It aggressively loops over every single `is_active=True` Equipment record.
2. For each node, it systematically queries exactly the **last 100 Sensor Readings** sorted sequentially by timestamp.
3. If the array length is functionally smaller than 10, the model instantly aborts predictions to prevent skew.
4. It feeds the 100-reading batch strictly into the `AnomalyDetector` singleton.
5. It mathematically partitions the output mapping it into the `HealthStatus` PostgreSQL table.
6. If the score plunges beneath `-0.15`, the task dynamically spawns the `AlertService` router before saving the record.
