from django.contrib import admin

from .models import Vendor, Category, Product, ProductReview, Address, Order, OrderItem

admin.site.register(Vendor)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_image']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_image', 'price', 'product_status', 'in_stock']
    list_editable = ['price', 'product_status', 'in_stock']


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'review', 'rating']
    list_editable = ['rating']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'city', 'state', 'status']
    list_editable = ['status']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'total', 'product_status']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'order_image', 'quantity']