# Inventory API Documentation

This document explains the RESTful interaction hooks exposing the Inventory models globally securely to external dashboards (like Next.js apps).

## `EquipmentViewSet`
File: `backend/inventory/api/views.py`

This fully authenticated Django Rest Framework `ModelViewSet` exposes all standard JSON CRUD operations natively.

**Core Methods & Behaviors:**
1. **Serialization**: It utilizes the `EquipmentSerializer` structurally to mathematically block read-only fields (like MAC addresses if obfuscated) while passing critical identifiers seamlessly to the React frontend.
2. **Filtering**: Authorized users can natively perform string queries on `equipment_type` to securely populate isolated UI dashboards.

## `MaintenanceLogViewSet`
File: `backend/inventory/api/views.py`

This endpoint exclusively provides historical diagnostic data. 

**Core Properties:**
1. **Creation Overrides**: The view structurally overrides the `perform_create` hook, forcing the `author` field to maliciously match the exact HTTP Request `User`. This dynamically prevents Technicians from mathematically spoofing repair logs.
