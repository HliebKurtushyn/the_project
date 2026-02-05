from django.db import models
from django.core.validators import MinValueValidator

from product.models import Product

from core.models import CustomUser


class Cart(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    session_key = models.CharField(max_length=40, null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def items(self):
        return self.cartitem_set.all()

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())


class CartItem(models.Model):
    id = models.AutoField(primary_key=True)

    #   Прив'язка до Cart, яка може бути:
    # - DB cart для логіненого юзера
    # - анонімний через session (тут буде лише DB для юзерів)

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')

    # Ціна буде отримуватись через зв'язок з Product (product.price)

    # Використав MinValueValidator, бо треба щоб мінімальне значення було 1
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Cart {self.cart.id}"

    # Використав @property щоб шаблони могли викликати як атрибут (cart_item.total_price)
    @property
    def total_price(self):
        return self.product.price * self.quantity

    def add_to_cart(self, quantity):
        self.quantity += quantity
        self.save(update_fields=['quantity'])

    def get_price(self):
        return self.product.price

    def get_total_price(self):
        return self.total_price


class SessionCartItem:
    def __init__(self, product, quantity):
        self.id = None               # у CartItem є id, тут можна None
        self.cart = None             # теж None
        self.product = product
        self.quantity = quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in SessionCart"

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def add_to_cart(self, quantity):
        self.quantity += quantity

    def get_price(self):
        return self.product.price

    def get_total_price(self):
        return self.total_price
