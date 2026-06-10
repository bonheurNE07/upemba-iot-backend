# Inventory Models Documentation

This document explains the physical asset catalog architecture powering the Upemba IoT pipeline.

## `Equipment` Model
File: `backend/inventory/models/equipment.py`

This model acts as the central planetary hub for all IoT devices physically tracked by the database.

**Fields:**
- `name`: A human-readable identifier (e.g., 'Solar Array East 1').
- `equipment_type`: A categorical structure mathematically isolating devices into `INVERTER`, `PANEL`, or `BATTERY` architectures.
- `mac_address`: The absolutely immutable physical radio identifier. This is mathematically utilized by the Mosquitto MQTT daemon to link autonomous IoT payloads directly to their master record gracefully.
- `installation_date`: Tracking hardware lifecycle decay.
- `is_active`: A boolean toggle allowing Administrators to permanently pause or silence telemetry from degraded nodes without executing irreversible SQL deletions.

## `MaintenanceLog` Model
File: `backend/inventory/models/maintenance.py`

This model tracks all physical human interaction with the IoT devices on the ground.

**Fields:**
- `equipment`: A cascading Foreign Key binding the log to a single piece of hardware.
- `author`: The absolute `User` model (typically mapped to a Ranger or Field Technician) responsible for the physical repairs.
- `timestamp`: Chronological tracking of precisely when the mechanical intervention occurred in reality.
- `description`: The initial issue encountered (e.g., "Critical Voltage Drop Triggered AI Alert").
- `action_taken`: The exact structural repair implemented.
