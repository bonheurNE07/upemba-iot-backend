# Telemetry Services Documentation

This document explicitly details the business logic and algorithms executed upon the Telemetry models.

## `AnomalyDetector` Service
File: `backend/telemetry/services/ml_service.py`

This python class wraps the `scikit-learn` Machine Learning pipeline into an easily actionable Django service.

**Mechanism:**
1. It imports the `IsolationForest` module natively.
2. It mathematically maps only specific fields (`temperature`, `voltage`, `vib_x`, `vib_y`, `vib_z`) into a NumPy matrix array.
3. It fits the model securely to the historical baseline data provided by the Celery task window.
4. It actively cross-verifies the absolute latest chronological reading to output the predicted sequence state.

## `AlertService` Service
File: `backend/telemetry/services/alert_service.py`

This isolated class physically orchestrates outgoing network transmissions (like SMTP Emails) whenever the system identifies equipment entering a `CRITICAL` state.

**Mechanism:**
1. It queries the `User` database for individuals specifically assigned the `TECHNICIAN` role.
2. It dynamically parses the anomaly severity metrics natively into an HTML email template.
3. It securely dispatches the warning via Django's core `EmailMultiAlternatives` framework, alerting humans natively independent of the web dashboard.
