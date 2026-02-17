from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Sum, Count

from .models import Booking


@staff_member_required
def admin_dashboard(request):
    # 💰 Total Revenue (only paid bookings)
    total_revenue = (
        Booking.objects
        .filter(is_paid=True)
        .aggregate(total=Sum('amount'))['total'] or 0
    )

    # 🎟 Total Tickets Sold
    total_tickets = Booking.objects.filter(is_paid=True).count()

    # 🎬 Most Popular Movies
    popular_movies = (
        Booking.objects
        .filter(is_paid=True)
        .values('movie__name')
        .annotate(total=Count('id'))
        .order_by('-total')[:5]
    )

    # 🏟 Busiest Theaters
    busy_theaters = (
        Booking.objects
        .filter(is_paid=True)
        .values('theater__name')
        .annotate(total=Count('id'))
        .order_by('-total')[:5]
    )

    context = {
        'total_revenue': total_revenue,
        'total_tickets': total_tickets,
        'popular_movies': popular_movies,
        'busy_theaters': busy_theaters,
    }

    return render(request, 'admin/dashboard.html', context)
