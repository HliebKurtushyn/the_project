from django.shortcuts import get_object_or_404
from product.models import Product
from cart.models import Cart, CartItem

def get_or_create_cart(request):
    if not request.session.session_key:
        request.session.save()
    session_key = request.session.session_key
    cart, _ = Cart.objects.get_or_create(session_key=session_key, is_active=True)
    return cart