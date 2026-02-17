from product.models import Product
from product.models import Category
from django.urls import reverse
from django.utils.safestring import mark_safe
import json


# Контекстний процесор для відображення недавно переглянутих товарів в усіх шаблонах автоматично
def recently_viewed(request):
    viewed_ids = request.session.get("recently_viewed", [])
    products = Product.objects.filter(id__in=viewed_ids)

    return {"recently_viewed": products}


# Для отримання категорій (бо використовується в base.html для відображення категорій в навігації)
def category_list(request):
    categories = Category.objects.all()

    # Допоміг ШІ, бо тут взагалі не розумів чому не працює як треба
    data = []
    list_url = reverse("product:product_list")
    for c in categories:
        try:
            count = c.products.count()
        except Exception:
            count = None
        data.append(
            {
                "name": c.name,
                "url": f"{list_url}?category={c.name}",
                "count": count,
            }
        )

    return {
        "categories": categories,
        "categories_json": mark_safe(json.dumps(data)),
    }
