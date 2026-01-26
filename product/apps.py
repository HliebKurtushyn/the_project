from django.apps import AppConfig
from django.utils import timezone

class ProductConfig(AppConfig):
    name = 'product'

    # При кожному запуску апки йде перевірка і видалення прострочених знижок
    def ready(self):
        from .models import Product
        expired = Product.objects.filter(discount_end_date__lt=timezone.now())
        for product in expired:
            product.discount = None
            product.discount_end_date = None
            product.save()