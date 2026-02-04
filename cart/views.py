from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from cart.models import Cart, CartItem
from product.models import Product
from .utils import get_cart



def cart_view(request):
    cart = get_cart(request)
    cart_items = cart.items

    return render(request, 'cart/cart_detail.html', {
        'cart': cart,
        'cart_items': cart_items
    })


@require_POST
def add_to_cart(request, product_id):
    cart = get_cart(request)
    product = get_object_or_404(Product, pk=product_id)

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        quantity = 1
    if quantity < 1:
        quantity = 1

    cart.add_item(product, quantity)

    return redirect("product:product_detail", id=product_id)


@require_POST
def remove_item(request, product_id):
    cart = get_cart(request)
    product = get_object_or_404(Product, pk=product_id)

    cart.remove_item(product)

    return redirect("cart:cart_detail")


@require_POST
def update_item(request, product_id):
    cart = get_cart(request)
    product = get_object_or_404(Product, pk=product_id)

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        quantity = 1
    if quantity < 1:
        quantity = 1

    if quantity > product.stock:
        quantity = product.stock
        messages.error(request, "Залишилось недостатньо товару на складі.")

    cart.update_item(product, quantity)


    return redirect("cart:cart_detail")
