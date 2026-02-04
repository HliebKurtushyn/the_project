from django.db import models

from .order_status import OrderStatus


class Order(models.Model):
    id = models.AutoField(primary_key=True)

    user = models.ForeignKey('core.CustomUser', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=OrderStatus.choices, default=OrderStatus.PENDING)

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())