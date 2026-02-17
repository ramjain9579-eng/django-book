from django.contrib import admin
from .models import Movie, Theater, Seat, Booking


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'genre', 'language']
    search_fields = ['name', 'cast']
    list_filter = ['genre', 'language']
    ordering = ['name']


@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    list_display = ['name', 'movie', 'time']
    list_filter = ['movie']


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['theater', 'seat_number', 'status', 'reserved_at']
    list_filter = ['status']   # ✅ USE REAL FIELD
    search_fields = ['seat_number']
    ordering = ['theater']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'movie',
        'theater',
        'seat',
        'amount',
        'is_paid',
        'booked_at'
    ]
    list_filter = ['movie', 'theater', 'is_paid']
    search_fields = ['user__username', 'movie_name']
