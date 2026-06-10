# Telemetry Models Documentation

This document explains the physical database tables mapping the IoT infrastructure.

## `SensorReading` Model
File: `backend/telemetry/models/reading.py`

This model acts as the primary historian for the ESP32. It records every telemetry packet exactly as it arrives. 

**Fields:**
- `equipment`: A Foreign Key specifically linking the data to the physical device located in the Inventory app.
- `temperature` & `voltage`: Core electrical health mappings.
- `vib_x`, `vib_y`, `vib_z`: Multi-axis structural vibration signatures.
- `timestamp`: An immutable `auto_now_add` DateTime mapping the physical arrival of the packet.

## `HealthStatus` Model
File: `backend/telemetry/models/health.py`

This model maps the direct output of our Scikit-Learn Isolation Forest machine learning algorithm.

**Fields:**
- `anomaly_score`: A raw float. Highly negative numbers represent severe deviations from the machine's baseline history.
- `status`: Categorical marker cleanly isolating the equipment into `NORMAL`, `WARNING`, or `CRITICAL` bands.
- `prediction_timestamp`: The exact timestamp the Celery Beat task executed the analytics operation against the `SensorReading` batches.
