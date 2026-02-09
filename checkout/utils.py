from django.db import transaction
from django.core.exceptions import MultipleObjectsReturned
from product.models import Product
from cart.models import Cart, CartItem, SessionCartItem

# Адаптери поставив щоб уніфіковувати роботу з оплатою для різних типів користувачів
class DBCheckoutAdapter:
    """Для залогіненого користувача"""
    def __init__(self, user):
        try:
            self.cart, _ = Cart.objects.get_or_create(user=user)
        except MultipleObjectsReturned:
            # Тут я зробив об'єднання дублікатів кошиків у один якщо вони є, бо таке ставалось
            with transaction.atomic():
                carts = list(Cart.objects.filter(user=user).order_by('-id'))
                primary = carts[0]
                duplicates = carts[1:]
                for dup in duplicates:
                    for item in list(dup.items.all()):
                        existing = CartItem.objects.filter(cart=primary, product=item.product).first()
                        if existing:
                            existing.quantity += item.quantity
                            existing.save()
                            item.delete()
                        else:
                            item.cart = primary
                            item.save()
                    dup.delete()
                self.cart = primary

    @property
    def items(self):
        return self.cart.items

    @property
    def total_price(self):
        return self.cart.total_price

    @property
    def items_list(self):
        if hasattr(self, 'items'):  # DB Cart
            return self.items.all()
        return self.items  # SessionCart

    def clear_cart(self):
        self.cart.items.all().delete()

    def add_item(self, product, quantity):
        item, created = CartItem.objects.get_or_create(cart=self.cart, product=product)
        if created:
            item.quantity = quantity
        else:
            item.quantity += quantity
        item.save()

    def remove_item(self, product):
        try:
            item = CartItem.objects.get(cart=self.cart, product=product)
            item.delete()
        except CartItem.DoesNotExist:
            pass

    def update_item(self, product, quantity):
        try:
            item = CartItem.objects.get(cart=self.cart, product=product)
            item.quantity = quantity
            item.save()
        except CartItem.DoesNotExist:
            pass


class SessionCheckoutAdapter:
    """Для анонімного користувача"""
    def __init__(self, request):
        if not request.session.session_key:
            request.session.save()
        self.session = request.session
        self.items_data = self.session.get("cart", {}).get("items", {})

    @property
    def items(self):
        items = []
        for product_id, data in self.items_data.items():
            product = Product.objects.get(pk=product_id)
            items.append(SessionCartItem(product, data["quantity"]))
        return items

    @property
    def total_price(self):
        return sum(item.get_price() for item in self.items)

    @property
    def items_list(self):
        return self.items

    def clear_cart(self):
        self.session["cart"] = {"items": {}}
        self.session.modified = True

    def add_item(self, product, quantity):
        product_id_str = str(product.id)
        if product_id_str in self.items_data:
            self.items_data[product_id_str]["quantity"] += quantity
        else:
            self.items_data[product_id_str] = {"quantity": quantity, "price": float(product.price)}
        self.session["cart"] = {"items": self.items_data}
        self.session.modified = True

    def remove_item(self, product):
        product_id_str = str(product.id)
        if product_id_str in self.items_data:
            del self.items_data[product_id_str]
            self.session["cart"] = {"items": self.items_data}
            self.session.modified = True

    def update_item(self, product, quantity):
        product_id_str = str(product.id)
        if product_id_str in self.items_data:
            self.items_data[product_id_str]["quantity"] = quantity
            self.session["cart"] = {"items": self.items_data}
            self.session.modified = True

# Повертає cart, а items тепер через cart.items
def get_cart(request):
    if request.user.is_authenticated:
        return DBCartAdapter(request.user)
    return SessionCartAdapter(request)