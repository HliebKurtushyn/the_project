from django.views.decorators.cache import cache_page
from functools import wraps


# Декоратор для кешування сторінок лише для анонімних користувачів
def cache_page_anonymous(timeout):
    def _decorator(view_func):
        cached = cache_page(timeout)(view_func)

        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                return view_func(request, *args, **kwargs)

            if request.GET.get("search") or request.GET.get("category"):
                return view_func(request, *args, **kwargs)

            return cached(request, *args, **kwargs)

        return _wrapped_view

    return _decorator
