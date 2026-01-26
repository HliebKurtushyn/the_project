from django.contrib import admin

from .models import Product, Category, Brand


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_categories', 'get_brand', 'size', 'description', 'price', 'discount_value', 'discount_end_date', 'stock')
    search_fields = ('name', 'discount_value', 'discount_end_date')
    list_filter = ('category', 'brand')
    ordering = ('-name',)

    def get_categories(self, obj):
        return ", ".join([c.name for c in obj.category.all()])
    get_categories.short_description = 'Categories'

    def get_brand(self, obj):
        if obj.brand:
            return obj.brand.name
        return None
    get_brand.short_description = 'Brand'


    def discount_value(self, obj):
        return obj.discount
    discount_value.short_description = 'Discount'

    def discount_end_date(self, obj):
        return obj.discount_end_date
    discount_end_date.short_description = 'Discount End Date'

# WIP
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

# WIP
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
