from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from cart.models import Cart, CartItem
from product.models import Product
from .utils import get_or_create_cart

@require_POST
def cart_view(request):
    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key

    cart, created = Cart.objects.get_or_create(session_key=session_key)
    cart_items = CartItem.objects.filter(cart=cart)

    if cart_items.exists() and not cart.is_active:
        cart.is_active = True
        cart.save(update_fields=['is_active'])

    return render(request, 'cart/cart_detail.html', {'cart': cart, 'cart_items': cart_items})


@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = get_or_create_cart(request)

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        quantity = 1
    if quantity < 1:
        quantity = 1

    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if created:
        item.quantity = quantity
        item.save(update_fields=['quantity'])
    else:
        item.add_to_cart(quantity)

    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or '/'
    return redirect(next_url)


@require_POST
def remove_item(request, product_id):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, pk=product_id)

    try:
        item = CartItem.objects.get(cart=cart, product=product)
        item.delete()
    except CartItem.DoesNotExist:
        pass

    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or '/'
    return redirect(next_url)


@require_POST
def update_item(request, product_id):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, pk=product_id)

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        quantity = 1
    if quantity < 1:
        quantity = 1

    try:
        item = CartItem.objects.get(cart=cart, product=product)
        item.quantity = quantity
        item.save(update_fields=['quantity'])
    except CartItem.DoesNotExist:
        pass

    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or '/'
    return redirect(next_url)