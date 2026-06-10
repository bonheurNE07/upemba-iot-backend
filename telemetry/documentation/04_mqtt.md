# MQTT Telemetry Daemon Documentation

This document unpacks the long-running script driving the edge-networking IoT pipelines.

## `mqtt_listener` Command
File: `backend/telemetry/management/commands/mqtt_listener.py`

This file is built upon Django's `BaseCommand` CLI structure but operates permanently in a generic `while True` loop listening to Mosquitto.

**Sequence of Operations:**
1. It utilizes the generic `paho.mqtt.client` library initialized explicitly into `VERSION2` callbacks to avoid legacy deprecation.
2. Upon startup, it securely anchors to the `upemba/sensors/+/telemetry` wildcard.
3. When payloads physically execute `on_message`, it unpacks the raw JSON byte array using massive `try/except` guard-rails to securely catch structurally invalid C++ ESP32 strings safely without crashing the single-threaded listener.
4. It resolves the Equipment Foreign Keys via `mac_address`.
5. It injects the `SensorReading` parameters natively into PostgreSQL before terminating the loop cycle.
