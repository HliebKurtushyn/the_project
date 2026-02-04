from django.utils.dateparse import parse_datetime
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from datetime import datetime

from cart.utils import get_cart, get_items
from .models import Order, OrderItem, OrderStatus, OrdersHistory

def checkout(request):
    cart = get_cart(request)
    cart_items = get_items(request, cart)

    if cart_items:
        pass
    else:
        messages.error(request, "Кошик пустий.")
        return redirect('cart:cart_detail')

    return render(request, 'checkout/checkout_detail.html', {
        'cart': cart,
        'cart_items': cart_items
    })


@require_POST
def checkout_confirm(request):
    user = request.user if request.user.is_authenticated else None
    cart = get_cart(request)
    cart_items = get_items(request, cart)

    if not cart_items:
        messages.error(request, "Помилка: Кошик пустий.")
        return redirect('cart:cart_detail')

    with transaction.atomic():
        order = Order.objects.create(user=user, status=OrderStatus.PENDING)

        order_items = [
            OrderItem(order=order, product=item.product, quantity=item.quantity, price=item.total_price)
            for item in cart_items
        ]
        OrderItem.objects.bulk_create(order_items)

        cart.clear_cart()

        request.session['last_checkout'] = {
            "order_id": order.id,
            "total_price": str(order.total_price)
        }

        if user:
            OrdersHistory.objects.create(
                user=user,
                order_data={
                    "order_id": order.id,
                    "created_at": order.created_at.isoformat(),
                    "status": order.status,
                    "total_price": str(order.total_price),
                }
            )
        else:
            request.session[f"order {order.id}"] = {
                "id": order.id,
                "created_at": order.created_at.isoformat(),
                "status": order.status,
                "total_price": str(order.total_price),
            }

        for item in order_items:
            item.product.stock -= item.quantity
            item.product.save()

    return redirect('checkout:checkout_success')


def checkout_success(request):
    last_checkout = request.session.get('last_checkout')

    if last_checkout:
        order_id = request.session.get('last_checkout')['order_id']
        if not order_id:
            messages.error(request, "Немає інформації про останнє замовлення.")
            return redirect('cart:cart_detail')

        total_price = request.session.get('last_checkout')['total_price']
        status = Order.objects.only('status').get(id=order_id).status
        items = OrderItem.objects.filter(id=order_id)

        return render(request, 'checkout/checkout_success.html', {
            'order_id': order_id,
            'items': items,
            'total_price': total_price,
            'status': status
        })

    else:
        messages.error(request, "Немає інформації про останнє замовлення.")
        return redirect('cart:cart_detail')


def orders_history(request):
    user = request.user if request.user.is_authenticated else None

    orders_list = []

    # Автентифікованим користувачам
    if user:
        orders_history_queryset = OrdersHistory.objects.filter(user=user).order_by('-id')
        if not orders_history_queryset.exists():
            return render(request, 'checkout/orders_history.html', {"orders": None})

        for history_record in orders_history_queryset:
            order_data = history_record.order_data or {}
            order_id = order_data.get('order_id') or order_data.get('id')

            raw_created_at = order_data.get('created_at')
            created_at_dt = None
            if isinstance(raw_created_at, str):
                created_at_dt = parse_datetime(raw_created_at)
            elif isinstance(raw_created_at, datetime):
                created_at_dt = raw_created_at

            order_items_for_order = OrderItem.objects.filter(order_id=order_id) if order_id else OrderItem.objects.none()

            orders_list.append({
                'order_id': order_id,
                'total_price': order_data.get('total_price'),
                'status': order_data.get('status'),
                'created_at': created_at_dt,
                'items': order_items_for_order,
            })

        return render(request, 'checkout/orders_history.html', {
            "orders": orders_list
        })

    # Неавтентифікованим користувачам
    session_orders_list = []

    orders_history_session_value = request.session.get('orders_history')
    if orders_history_session_value:
        if isinstance(orders_history_session_value, list):
            session_orders_list.extend(orders_history_session_value)
        elif isinstance(orders_history_session_value, dict):
            session_orders_list.append(orders_history_session_value)

    for session_key, session_value in request.session.items():
        if isinstance(session_key, str) and session_key.startswith('order ') and isinstance(session_value, dict):
            session_orders_list.append(session_value)

    last_checkout_session = request.session.get('last_checkout')
    if last_checkout_session and isinstance(last_checkout_session, dict):
        session_orders_list.append(last_checkout_session)

    if not session_orders_list:
        return render(request, 'checkout/orders_history.html', {"orders": None})

    seen_order_ids = set()
    for raw_order in session_orders_list:
        order_id = raw_order.get('order_id') or raw_order.get('id')
        if not order_id:
            continue
        if order_id in seen_order_ids:
            continue
        seen_order_ids.add(order_id)

        raw_created_at = raw_order.get('created_at')
        created_at_dt = None
        if isinstance(raw_created_at, str):
            created_at_dt = parse_datetime(raw_created_at)
        elif isinstance(raw_created_at, datetime):
            created_at_dt = raw_created_at

        order_status = raw_order.get('status')
        if not order_status:
            try:
                order_status = Order.objects.only('status').get(id=order_id).status
            except Order.DoesNotExist:
                order_status = None

        order_items_for_order = OrderItem.objects.filter(order_id=order_id)

        created_at_dt = created_at_dt.strftime("%d.%m.%Y %H:%M")
        orders_list.append({
            'order_id': order_id,
            'total_price': raw_order.get('total_price'),
            'status': order_status,
            'created_at': created_at_dt,
            'items': order_items_for_order,
        })

    return render(request, 'checkout/orders_history.html', {
        "orders": orders_list
    })
