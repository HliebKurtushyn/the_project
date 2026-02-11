from django.shortcuts import get_object_or_404, render
from product.models import Product

def product_detail_view(request, id):
    product = get_object_or_404(Product.objects.select_related('brand').prefetch_related('category'), id=id)

    return render(request, 'product/product.html', {'product': product})

def product_list_view(request):
    products = Product.objects.all()
    return render(request, 'product/product_list.html', {'products': products})