from django.db import models


class OrdersHistory(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('core.CustomUser', on_delete=models.CASCADE, null=True, blank=True)
    order_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)