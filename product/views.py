from django.shortcuts import get_object_or_404, render
from product.models import Product
from core.cache_utils import cache_page_anonymous


def product_detail_view(request, id):
    product = get_object_or_404(
        Product.objects.select_related("brand").prefetch_related("category"), id=id
    )
    viewed_ids = request.session.get("recently_viewed", [])

    if product.id in viewed_ids:
        viewed_ids.remove(product.id)
    viewed_ids.insert(0, product.id)

    request.session["recently_viewed"] = viewed_ids[:5]
    request.session.modified = True

    return render(
        request,
        "product/product.html",
        {"product": product},
    )


@cache_page_anonymous(60 * 10)
def product_list_view(request):
    products = Product.objects.all()

    search = request.GET.get("search")
    if search:
        products = products.filter(name__icontains=search)

    category_name = request.GET.get("category")
    if category_name:
        products = products.filter(category__name__iexact=category_name)

    return render(
        request,
        "product/product_list.html",
        {"products": products, "current_category": category_name, "search": search},
    )
