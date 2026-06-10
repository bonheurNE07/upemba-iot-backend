# Users & Authentication Documentation

This document traces the custom authentication overrides governing the IoT Backend natively via Cookiecutter Django and `django-allauth`.

## `User` Model
File: `backend/users/models.py`

The Upemba architecture specifically inherits from Django's generic `AbstractUser` to formally structure custom Role-Based Access Control.

**Fields:**
- `role`: A strictly enforced `TextChoices` structure separating accounts into `ADMIN`, `TECHNICIAN` (can receive MQTT Critical Alert emails), and `RANGER`.
- `name`: Collapsing the legacy `first_name` and `last_name` arrays into a single string to universally support structural global names.

## Identity Providers (`django-allauth`)
File: `config/settings/base.py`

This repository overrides the standard Django login frameworks natively dynamically leveraging the `allauth` plugins.

**Authentication Mechanisms:**
- **Email Primary vs Username**: In `base.py`, `ACCOUNT_LOGIN_METHODS = {"username"}` forces users to login via Username instead of Email. However, the custom Next.js frontend or standard views can be rapidly swapped.
- **Mandatory Validation**: `ACCOUNT_EMAIL_VERIFICATION = "mandatory"` physically prevents unverified email accounts from traversing into internal REST endpoints.
- **Bypass Flags**: For direct IoT Edge device connections bypassing the browser, JSON Web Tokens (via `rest_framework.authtoken`) are mapped inside `ACCOUNT_ADAPTER`.
