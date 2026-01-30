from django.db import models
from django.core.validators import MinValueValidator

from product.models import Product

# Кошик базується на сесії, а не користувачі
class Cart(models.Model):
    id = models.AutoField(primary_key=True)

    session_key = models.CharField(max_length=40, null=True, blank=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"Cart {self.id}"


class CartItem(models.Model):
    id = models.AutoField(primary_key=True)

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')

    # Ціна буде отримуватись через зв'язок з Product (product.price)

    # Використав MinValueValidator, бо треба щоб мінімальне значення було 1
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Cart {self.cart.id}"

    def get_total_price(self):
        return self.product.price * self.quantity

    def add_to_cart(self,quantity):
        self.quantity += quantity
        self.save(update_fields=['quantity'])