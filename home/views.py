from django.shortcuts import render
from product.models import Product, Category
from core.cache_utils import cache_page_anonymous


@cache_page_anonymous(60 * 10)
def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    return render(
        request, "home/home.html", {"products": products, "categories": categories}
    )
