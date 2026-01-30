from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .models import Product
from cart.models import Cart, CartItem

from cart.utils import get_or_create_cart

def product_detail_view(request, id:int):
    product = get_object_or_404(Product, id=id)

    return render(request, "product/product.html", {"product": product})
