from django.contrib import admin
from .models import Category, Dish, Order, OrderItem

admin.site.register(Category)
admin.site.register(Dish)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('dish', 'quantity', 'price')
    can_delete = False

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'phone_number', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer_name', 'phone_number')
    readonly_fields = ('customer_name', 'phone_number', 'address', 'total_price', 'created_at')
    inlines = [OrderItemInline]