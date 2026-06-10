import logging

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


class AlertService:
    """
    This service is responsible for immediately contacting humans when the Machine Learning
    model detects a dangerous anomaly.
    """
    
    @staticmethod
    def trigger_critical_alert(equipment_name, score, timestamp):
        """
        Sends an email alert to the configured park rangers/admins regarding a CRITICAL 
        equipment health status. It sends a nice HTML email, with a plain-text fallback.
        """
        
        # 1. Safety Check: Only send emails if we have an email server configured
        if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
            logger.warning("SMTP credentials not provided. Skipping email dispatch.")
            return

        subject = f"CRITICAL ALERT: {equipment_name} Failure Predicted"

        # 2. Prepare the plain-text message (used if the user's email client blocks HTML)
        message = (
            f"URGENT: Upemba Predictive Maintenance System has flagged "
            f"a Critical Health Status for '{equipment_name}'.\n\n"
            f"Detection Timestamp: {timestamp}\n"
            f"Anomaly Score: {score}\n\n"
            f"Immediate physical inspection by field rangers is heavily recommended."
        )

        # 3. Prepare the rich HTML email (looks nicer)
        # We pass these variables into a Django HTML template to render the email beautifully
        context = {
            "equipment_name": equipment_name,
            "score": score,
            "timestamp": timestamp,
        }
        html_message = render_to_string("telemetry/email/critical_alert.html", context)

        from users.models import User

        # 4. Figure out WHO to send the email to
        # Look in our database for users whose role is ADMIN or TECHNICIAN, and who have an email address.
        recipients = (
            User.objects.filter(
                role__in=[User.Role.ADMIN, User.Role.TECHNICIAN],
                is_active=True,
                email__isnull=False,
            )
            .exclude(email="")
            .values_list("email", flat=True)
        )

        recipient_list = list(recipients)

        # 5. Fallback in case no users are configured yet
        if not recipient_list:
            logger.warning("No Technicians/Admins found in DB. Falling back to settings.ADMINS.")
            recipient_list = [admin[1] for admin in settings.ADMINS]
            
            # If even settings.ADMINS is empty, we give up.
            if not recipient_list:
                logger.warning("No recipients available for critical alerts.")
                return

        # 6. Actually send the email using Django's built-in mailer
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipient_list,
                html_message=html_message,
                fail_silently=False,
            )
            logger.info(f"Critical HTML alert email successfully dispatched to {recipient_list}")
        except Exception as e:
            logger.exception(f"Failed to send critical HTML alert email: {e}")
