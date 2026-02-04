from django.urls import path

from . import views

app_name = 'checkout'

urlpatterns = [
    path('', views.checkout, name='checkout_view'),
    path('confirm/', views.checkout_confirm, name='checkout'),
    path('success/', views.checkout_success, name='checkout_success'),
]