from django.urls import path

from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('category_list/', views.category_list_view, name='category_list'),
    path('category_product_list/<int:id>/', views.category_product_list_view, name='category_product_list'),

    path('product_list/', views.product_list_view, name='product_list'),
    path('product_detail/<int:id>/', views.product_detail_view, name='product_detail'),
    path('filter_product/', views.filter_product, name='filter_product'),

    # Cart
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('delete_item_from_cart/', views.delete_item_from_cart, name='delete_item_from_cart'),


    # Payment
    path('checkout/', views.checkout_view, name='checkout'),
]