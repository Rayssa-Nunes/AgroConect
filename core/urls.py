from django.urls import path, include

from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('category_list/', views.category_list_view, name='category_list'),
    path('category_product_list/<int:id>/', views.category_product_list_view, name='category_product_list'),

    path('product_list/', views.product_list_view, name='product_list'),
    path('product_detail/<int:id>/', views.product_detail_view, name='product_detail'),
    path('filter_product/', views.filter_product, name='filter_product'),

    path('vendor_list/', views.vendor_list_view, name='vendor_list'),

    # Cart
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('delete_item_from_cart/', views.delete_item_from_cart, name='delete_item_from_cart'),


    # Payment
    path('checkout/', views.checkout_view, name='checkout'),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('payment_success/', views.payment_success_view, name='payment_success'),
    path('payment_failed/', views.payment_failed_view, name='payment_failed'),
]