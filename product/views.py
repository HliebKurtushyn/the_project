from django.shortcuts import render, get_object_or_404

from product.models import Product


def product_detail_view(request, id:int):
    product = get_object_or_404(Product, id=id)

    return render(request, "product/product.html", {"product": product})