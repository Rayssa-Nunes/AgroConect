from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, Count
from django.contrib import messages
from django.utils.timezone import now
from django.http import JsonResponse
from django.contrib.humanize.templatetags.humanize import naturaltime

from django.db.models.functions import Coalesce, ExtractMonth, ExtractYear
from django.utils.translation import gettext as _ 
import calendar
from decimal import Decimal

from render_block import render_block_to_string

from core.models import Vendor, Order, OrderItem, Product, Category, STATUS
from accounts.models import CustomUser
from .forms import AddProductForm


@login_required
def vendor_dashboard_view(request):
    if not request.user.has_perm('core.view_vendor_dashboard'):
        messages.error(request, 'Você não tem permissão para acessar esta página.')
        return redirect('home')
    
    all_users = CustomUser.objects.all().count()
    products_in_cart = OrderItem.objects.filter(
        product__user=request.user, order__paid_status=False).aggregate(total_quantity=Sum('quantity')
    )
    revenue = OrderItem.objects.filter(
        product__user=request.user, 
        order__paid_status=True).aggregate(total_revenue=Sum(F('quantity') * F('product__price'))
    )

    this_month = now().month
    this_year = now().year
    monthly_revenue = OrderItem.objects.filter(
        product__user=request.user,
        order__created_at__month=this_month,
        order__created_at__year=this_year,
        order__paid_status=True,
    ).aggregate(
        total_revenue=Coalesce(Sum(F('product__price') * F('quantity')), Decimal('0.00'))
    )

    # new_user_registered = CustomUser.objects.order_by('-date_joined').first()
    # last_product_registered = Product.objects.filter(user=request.user).latest('date')
    # new_order_registered = OrderItem.objects.filter(product__user=request.user).order_by('-order__created_at').first()

    # order_items = OrderItem.objects.filter(product__user=request.user).annotate(month=ExtractMonth('order__created_at')).values('month').annotate(count=Count('id')).values('month', 'count')
    order_items = OrderItem.objects.filter(product__user=request.user, order__paid_status=True).annotate(
        year=ExtractYear('order__created_at'),
        month=ExtractMonth('order__created_at')
            ).values('month').annotate(
                total_quantity=Sum('quantity')
            ).values('month', 'total_quantity').order_by('year', 'month')
    print(order_items)

    month = []
    total_order_items = []
    for i in order_items:
        month.append(_(calendar.month_name[i['month']]))
        total_order_items.append(i['total_quantity'])

    print(month)
    print(total_order_items)

    context = {
        'all_users': all_users,
        'products_in_cart': products_in_cart,
        'revenue': revenue,
        'monthly_revenue': monthly_revenue,
        # 'new_user_registered': naturaltime(new_user_registered.date_joined),
        # 'last_product_registered': naturaltime(last_product_registered.date),
        # 'new_order_registered': naturaltime(new_order_registered.order.created_at),
        'month': month,
        'total_order_items': total_order_items,
    }

    print(products_in_cart)

    return render(request, 'useradmin/vendor_dashboard.html', context)


def products(request):
    status = request.GET.get('status', None)
        
    all_products = Product.objects.filter(user=request.user).order_by('-id')
    all_categories = Category.objects.all()

    context = {
        'all_products': all_products,
        'all_categories': all_categories,
        'status_choices': STATUS,
    }

    if status is not None:
        print(status)
        
        filtered_products = Product.objects.filter(user=request.user, product_status=status)
        context["all_products"] = filtered_products.order_by('-id')
        data = render_block_to_string('useradmin/products.html', 'products', context)
        return JsonResponse({'data': data})
        # return HttpResponse(data)

    return render(request, 'useradmin/products.html', context)


def add_product(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            vendor = Vendor.objects.get(user=request.user)
            new_form.vendor = vendor
            new_form.save()
            messages.success(request, 'Produto cadastrado com sucesso!')
            return redirect('vendor_dashboard')
        else:
            messages.error(request, 'Erro ao cadastrar produto. Verifique os campos abaixo.')
    else:
        form = AddProductForm()
    return render(request, 'useradmin/add_product.html', {'form': form})


def update_product(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():

            if not form.cleaned_data['image']:
                form.cleaned_data['image'] = product.image
                
            updated_product = form.save(commit=False)
            updated_product.user = request.user
            vendor = Vendor.objects.get(user=request.user)
            updated_product.vendor = vendor
            updated_product.save()
            messages.success(request, 'Produto atualizado com sucesso!')
            return redirect('update_product', product.pk)
        else:
            messages.error(request, 'Erro ao atualizar produto. Verifique os campos abaixo.')
    else:
        form = AddProductForm(instance=product)
    
    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'useradmin/update_product.html', context)


def delete_product(request, pk):
    product = Product.objects.get(pk=pk)

    product.delete()

    messages.success(request, 'Produto deletado com sucesso!')
    return redirect('products')


def orders(request):
    orders = Order.objects.filter(orderitem__product__user=request.user).order_by('-id').distinct()
    
    paid_status = request.GET.get('paid_status')
    product_status = request.GET.get('product_status')
    print(paid_status)
    
    if paid_status:
        paid_status_bool = True if paid_status == 'True' else False
        orders = orders.filter(paid_status=paid_status_bool)
    
    if product_status:
        orders = orders.filter(product_status=product_status)
    
    status_choices = Order._meta.get_field('product_status').choices

    context = {
        'orders': orders,
        'status_choices': status_choices,
        'selected_product_status': product_status,
        'paid_status': paid_status_bool if paid_status else None
    }
    
    return render(request, 'useradmin/orders.html', context)


def order_detail(request, id):
    order = get_object_or_404(Order, id=id)
    order_items = OrderItem.objects.filter(order=order)
    status_choices = Order._meta.get_field('product_status').choices

    if request.method == 'POST':
        status = request.POST.get('status')
        
        status_list = [choice[0] for choice in Order._meta.get_field('product_status').choices]
        if status in status_list:
            order.product_status = status
            order.save()
            return JsonResponse({'status': status.capitalize()})
        else:
            return JsonResponse({'error': 'Status inválido'}, status=400)

    context = {
        'order': order,
        'order_items': order_items,
        'status_choices': status_choices,
    }
    return render(request, 'useradmin/order_detail.html', context)
