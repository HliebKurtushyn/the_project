from django.shortcuts import render
from product.models import Product, Category


def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    return render(
        request, "home/home.html", {"products": products, "categories": categories}
    )
