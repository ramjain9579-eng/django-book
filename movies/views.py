from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import transaction
from django.contrib import messages

from .models import Movie, Theater, Seat, Booking
from .utils import release_expired_seats


# =========================
# MOVIE LIST (HOME PAGE)
# =========================
def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movies/movie_list.html', {
        'movies': movies
    })


# =========================
# MOVIE DETAIL
# =========================
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    return render(request, 'movies/movie_detail.html', {
        'movie': movie
    })


# =========================
# THEATER LIST
# =========================
def theater_list(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    theaters = Theater.objects.filter(movie=movie)

    return render(request, 'movies/theater_list.html', {
        'movie': movie,
        'theaters': theaters
    })


# =========================
# BOOK SEATS (WITH TIMEOUT)
# =========================
@login_required
def book_seats(request, theater_id):

    # 🔑 release expired seats first
    release_expired_seats()

    theater = get_object_or_404(Theater, id=theater_id)
    seats = Seat.objects.filter(theater=theater)

    if request.method == "POST":
        selected_seats = request.POST.getlist('seats')

        if not selected_seats:
            messages.error(request, "Please select at least one seat.")
            return redirect('book_seats', theater_id=theater.id)

        try:
            with transaction.atomic():
                for seat_id in selected_seats:
                    seat = Seat.objects.select_for_update().get(
                        id=seat_id,
                        theater=theater
                    )

                    if seat.status != 'available':
                        messages.error(request, f"Seat {seat.seat_number} already booked.")
                        return redirect('book_seats', theater_id=theater.id)

                    seat.status = 'reserved'
                    seat.reserved_at = timezone.now()
                    seat.user = request.user
                    seat.save()

            return redirect('payment_success')

        except Exception as e:
            messages.error(request, "Something went wrong. Try again.")
            return redirect('book_seats', theater_id=theater.id)

    return render(request, 'movies/book_seats.html', {
        'theater': theater,
        'seats': seats
    })


# =========================
# PAYMENT SUCCESS
# =========================
@login_required
def payment_success(request):

    reserved_seats = Seat.objects.filter(
        user=request.user,
        status='reserved'
    )

    with transaction.atomic():
        booking = Booking.objects.create(
            user=request.user,
            total_price=sum(seat.price for seat in reserved_seats),
            booking_time=timezone.now()
        )

        for seat in reserved_seats:
            seat.status = 'booked'
            seat.reserved_at = None
            seat.save()
            booking.seats.add(seat)

    return render(request, 'movies/payment_success.html', {
        'booking': booking
    })


# =========================
# PAYMENT FAILED
# =========================
@login_required
def payment_failed(request):

    Seat.objects.filter(
        user=request.user,
        status='reserved'
    ).update(
        status='available',
        reserved_at=None,
        user=None
    )

    return render(request, 'movies/payment_failed.html')
