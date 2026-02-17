from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


# =========================
# MOVIE MODEL
# =========================
class Movie(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="movies/")
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    cast = models.TextField()
    description = models.TextField(blank=True, null=True)
    genre = models.CharField(max_length=50)
    language = models.CharField(max_length=50)
    trailer_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


# =========================
# THEATER MODEL
# =========================
class Theater(models.Model):
    name = models.CharField(max_length=255)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    time = models.DateTimeField()

    def __str__(self):
        return f"{self.name} - {self.movie.name}"


# =========================
# SEAT MODEL (WITH TIMEOUT)
# =========================
class Seat(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('booked', 'Booked'),
    )

    theater = models.ForeignKey(
        Theater,
        on_delete=models.CASCADE,
        related_name='seats'
    )

    seat_number = models.CharField(max_length=10)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='available'
    )

    reserved_at = models.DateTimeField(null=True, blank=True)

    @property
    def is_booked(self):
        return self.status == 'booked'

    @property
    def is_reserved(self):
        return self.status == 'reserved'

    def is_reservation_expired(self):
        if self.status != 'reserved' or not self.reserved_at:
            return False

        return timezone.now() > self.reserved_at + timedelta(minutes=5)

    def __str__(self):
        return f"{self.seat_number} - {self.status}"


# =========================
# BOOKING MODEL
# =========================
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)

    seat = models.OneToOneField(Seat, on_delete=models.CASCADE)

    movie_name = models.CharField(max_length=100)
    amount = models.IntegerField()
    is_paid = models.BooleanField(default=False)

    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie_name}"
