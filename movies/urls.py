from django.urls import path
from . import views
from .admin_views import admin_dashboard

urlpatterns = [

    # ==========================
    # MOVIE & THEATER ROUTES
    # ==========================
    path('', views.movie_list, name='movie_list'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('theaters/<int:movie_id>/', views.theater_list, name='theater_list'),

    # ==========================
    # SEAT BOOKING & PAYMENT
    # ==========================
    path('book-seats/<int:theater_id>/', views.book_seats, name='book_seats'),

    # ==========================
    # PAYMENT RESULT HANDLING
    # ==========================
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-failed/', views.payment_failed, name='payment_failed'),

    # ==========================
    # ADMIN DASHBOARD (ANALYTICS)
    # ==========================
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
]
