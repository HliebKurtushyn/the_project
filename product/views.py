from django.shortcuts import get_object_or_404, render
from product.models import Product


def product_detail_view(request, id):
    product = get_object_or_404(
        Product.objects.select_related("brand").prefetch_related("category"), id=id
    )
    recently_viewed = request.session.get("recently_viewed", [])

    if product.id in recently_viewed:
        recently_viewed.remove(product.id)
    recently_viewed.insert(0, product.id)

    request.session["recently_viewed"] = recently_viewed[:5]
    request.session.modified = True

    return render(
        request,
        "product/product.html",
        {"product": product, "recently_viewed": recently_viewed},
    )
