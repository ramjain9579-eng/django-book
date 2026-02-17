from datetime import timedelta
from django.utils import timezone
from .models import Seat

# Seat reservation timeout (in minutes)
RESERVATION_TIMEOUT = 5


def release_expired_seats():
    """
    Release seats that were reserved but not paid
    within the timeout period.
    """
    expiry_time = timezone.now() - timedelta(minutes=RESERVATION_TIMEOUT)

    Seat.objects.filter(
        status='reserved',
        reserved_at__lt=expiry_time
    ).update(
        status='available',
        reserved_at=None
    )
