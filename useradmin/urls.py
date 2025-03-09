from django.urls import path
from . import views

urlpatterns = [
    path('vendor_dashboard/', views.vendor_dashboard_view, name='vendor_dashboard'),
    path('products/', views.products, name='products'),
    path('add_product/', views.add_product, name='add_product'),
    path('update_product/<pk>/', views.update_product, name='update_product'),
    path('delete_product/<pk>/', views.delete_product, name='delete_product'),

    path('orders/', views.orders, name='orders'),
    path('order_detail/<id>/', views.order_detail, name='order_detail'),
]