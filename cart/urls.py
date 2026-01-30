from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    path('view/', views.cart_view, name='cart_detail'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', views.remove_item, name='remove_from_cart'),
    path('update/<int:product_id>/', views.update_item, name='update_cart_item'),
]