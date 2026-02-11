from product.models import Product


# Контексттний процесор для відображення недавно переглянутих товарів в усіх шаблонах автоматично
def recently_viewed(request):
    viewed_ids = request.session.get("recently_viewed", [])
    products = Product.objects.filter(id__in=viewed_ids)

    return {"recently_viewed_products": products}
