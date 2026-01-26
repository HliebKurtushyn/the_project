from django.db import models
from django.db.models import IntegerField


class Product(models.Model):
    name = models.CharField(max_length=100)

    category = models.ManyToManyField('product.Category', related_name='products', default="test_category")
    brand = models.ManyToManyField('product.Brand', related_name='products', default="test_brand")

    size = models.CharField(max_length=20, default="No size specified.")
    description = models.TextField(default="No description available.")
    image = models.ImageField(upload_to='products/')

    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = IntegerField(max_length=3, default=0)
    discount_end_date = models.DateField(null=True, blank=True)

    stock = models.IntegerField(max_length=5, default=0)


    def __str__(self):
        return self.name