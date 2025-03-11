from .models import Category, Product, Vendor
from location.models import Fair

from django.db.models import Min, Max

from .cart import Cart

def default(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    vendors = Vendor.objects.all()
    fairs = Fair.objects.all()

    min_max_price = Product.objects.aggregate(Min('price'), Max('price'))

    # Total quantity of products in the cart
    cart = Cart(request)
    qty_total_products = cart.get_total_products()

    return {
        'categories': categories,
        'products_all': products,
        'min_max_price': min_max_price,
        'vendors': vendors,
        'qty_total_products': qty_total_products,
        'all_fairs': fairs,
    }