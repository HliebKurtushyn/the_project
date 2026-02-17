from django.db import models
from .brand import Brand


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    category = models.ManyToManyField(
        "product.Category", related_name="products", blank=True
    )
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, related_name="products", null=True, blank=True
    )

    size = models.CharField(max_length=20, default="No size specified.")
    description = models.TextField(default="No description available.")

    image = models.ImageField(upload_to="products/", blank=True, null=True)

    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, null=True, blank=True
    )
    discount_end_date = models.DateField(null=True, blank=True)

    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name
