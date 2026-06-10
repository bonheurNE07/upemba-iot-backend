from .models import User

def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    return User.objects.count()
