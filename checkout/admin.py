from django.contrib import admin

from checkout.models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'status', 'total_price')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'user__email', 'id')
    readonly_fields = ('created_at', 'total_price')

    def total_price(self, obj):
        return obj.total_price
    total_price.short_description = 'Total Price'
