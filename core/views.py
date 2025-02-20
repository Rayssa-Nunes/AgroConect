from django.shortcuts import render, redirect
from django.db.models import Q, Avg, Count

from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

from . import models

from .cart import Cart
from .forms import AddressForm

def home(request):
    return render(request, 'core/home.html')


def category_list_view(request):
    # categories = models.Category.objects.annotate(
    # product_count=Count('products', filter=Q(products__product_status='publicado'))).order_by('-product_count')

    categories = models.Category.objects.all()

    context = {
        'categories': categories,
    }
    return render(request, 'core/category_list.html', context)


def category_product_list_view(request, id):
    category = models.Category.objects.get(pk=id)
    products = models.Product.objects.filter(category=category, product_status='publicado').order_by('-id')

    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'core/category_product_list.html', context)


def product_list_view(request):
    products = models.Product.objects.filter(product_status='publicado')
    
    context = {
        'products': products,
    }
    return render(request, 'core/product_list.html', context)


def product_detail_view(request, id):
    product = models.Product.objects.get(id=id, product_status='publicado')
    reviews = product.reviews.all()

    average_rating = product.reviews.aggregate(Avg('rating'))['rating__avg']
    average_percentage = (average_rating / 5) * 100 if average_rating else 0

    vendor = product.vendor
    vendor_address = vendor.user.address.filter(status=True).first()

    related_products = models.Product.objects.filter(
        category=product.category,
        product_status='publicado'
    ).exclude(id=product.id)

    context = {
        'product': product,
        'reviews': reviews,
        # 'average_rating': average_rating,
        'average_percentage': int(average_percentage),
        'vendor': vendor,
        'vendor_address': vendor_address,
        'related_products': related_products,
    }

    return render(request, 'core/product_detail.html', context)


def filter_product(request):
    categories = request.GET.getlist('category[]', [])
    vendors = request.GET.getlist('vendor[]', [])
    min_price = request.GET.get('min_price', None)
    max_price = request.GET.get('max_price', None)

    filters = Q(product_status='publicado')

    if min_price is not None and max_price is not None:
        filters &= Q(price__gte=min_price, price__lte=max_price)

    if categories:
        filters &= Q(category__id__in=categories)

    if vendors:
        filters &= Q(vendor__id__in=vendors)

    products = models.Product.objects.filter(filters).order_by('-id').distinct()

    data = render_to_string('core/async/product_list.html', {'products': products})
    return JsonResponse({'data': data})


def add_to_cart(request):
    product_id = request.GET['id']
    product_qty = request.GET['quantity']

    cart = Cart(request)
    cart.add(product_id, product_qty)

    qty_total_products = cart.get_total_products()

    return JsonResponse({'qty_total_products': qty_total_products})


def cart_view(request):
    cart = Cart(request)
    products, total = cart.get()

    context = {
        'products': products,
        'total': total
    }

    return render(request, 'core/cart.html', context)


def update_cart(request):
    product_id = request.GET['id']
    product_qty = request.GET['quantity']

    cart = Cart(request)
    id, subtotal = cart.update(product_id, product_qty)

    products_from_cart, total = cart.get()
    qty_total_products = cart.get_total_products()

    data = {
        'product': {
            'id': id,
            'subtotal': subtotal,
        },
        'total': total,
        'qty_total_products': qty_total_products,
    }

    # print(data)

    return JsonResponse(data)


def delete_item_from_cart(request):
    product_id = request.GET['id']

    cart = Cart(request)
    cart.delete(product_id)

    products_from_cart, total = cart.get()
    qty_total_products = cart.get_total_products()

    data = render_to_string('core/async/cart.html', {
        'products': products_from_cart, 
        'total': total, 
        'qty_total_products': qty_total_products
    })
    
    return JsonResponse({
        'data': data, 
        'total': total, 
        'qty_total_products': qty_total_products
    })


@login_required(redirect_field_name="vendor_login", login_url='vendor_login')
def checkout_view(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.status = True
            address.save()

            return redirect('checkout')

    else:
        cart = Cart(request)
        products, total = cart.get()

        try:
            address = models.Address.objects.get(user=request.user, status=True)
        except models.Address.DoesNotExist:
            address = None

        address_form = AddressForm()

        context = {
            'products': products,
            'total': total,
            'address': address,
            'address_form': address_form,
        }

        return render(request, 'core/checkout.html', context)