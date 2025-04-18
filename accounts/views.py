from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from core.models import Vendor, Customer
from core.utils import add_permission
from core.forms import  VendorDetailsForm, AddressForm

from .tokens import account_activation_token
from .models import CustomUser
from .forms import RegisterForm, LoginForm

from core.cart import Cart


# from django.utils.timezone import now
# from django.contrib.humanize.templatetags.humanize import naturaltime

def activateEmail(request, user, to_email):
    mail_subject = 'Ative sua conta AgroConect.'
    message = render_to_string('mail/email_activate.html', {
        'user': user,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    
    # messages.success(request, f'Olá {user.username}, por favor vá para o email {to_email} e clique no link de ativação para confirmar o seu cadastro no AgroConect. <b>Nota:</b> Verifique sua caixa de spam.')

    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        # messages.success(request, 'E-mail de ativação enviado com sucesso!')
        messages.success(request, 'Cadastro realizado com sucesso. Verifique seu e-mail para ativar sua conta!')
    else:
        messages.error(request, f'Problema ao tentar enviar email para {to_email}, cheque se o email informado está correto.')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, CustomUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Conta ativada com sucesso! Você pode fazer login agora.')
        if hasattr(user, 'vendor') and user.has_perm('core.view_vendor_dashboard'):
            print('VENDOR')
            return redirect('vendor_login')
        elif hasattr(user, 'customer') and user.has_perm('core.view_customer_dashboard'):
            return redirect('customer_login')
    else:
        messages.error(request, 'O link de ativação é inválido.')
        return redirect('home')
    

def vendor_register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        vendor_form = VendorDetailsForm(request.POST)
        address_form = AddressForm(request.POST)

        if form.is_valid() and vendor_form.is_valid() and address_form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            vendor = vendor_form.save(commit=False)
            vendor.user = user 
            vendor.save()

            address = address_form.save(commit=False)
            address.user = user
            address.status = True
            address.save()
            
            add_permission(user, Vendor, 'view_vendor_dashboard')

            activateEmail(request, user, form.cleaned_data.get('email'))

            # messages.success(request, 'Cadastro realizado com sucesso. Verifique seu e-mail para ativar sua conta!')
            return redirect('/')
        else:
            messages.error(request, 'Verifique os erros abaixo.')
            # if form.errors or vendor_form.errors or address_form.errors:
            #     for error_list in [form.errors, vendor_form.errors, address_form.errors]:
            #         for field, errors in error_list.items():
            #             for error in errors:
            #                 messages.error(request, f"{error}")
    else:
        form = RegisterForm()
        vendor_form = VendorDetailsForm()
        address_form = AddressForm()

    return render(request, 'accounts/vendor_register.html', {
        'form': form,
        'vendor_form': vendor_form,
        'address_form': address_form,
    })


def vendor_login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.has_perm('core.view_vendor_dashboard'):
                    print('tem permissão')
                    auth_login(request, user)
                
                    if 'cart' in request.session:
                        Cart(request)._save_cart_to_db()

                    return redirect('vendor_dashboard')
                else:
                    messages.error(request, 'Você não tem acesso a esta página. Registre-se.')
                    return redirect('vendor_register')
            else:
                messages.error(request, 'Credenciais inválidas. Tente novamente.')
    else:
        form = LoginForm()
    return render(request, 'accounts/vendor_login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('home') 


def customer_register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            Customer.objects.create(user=user)
            add_permission(user, Customer, 'view_customer_dashboard')

            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('/')
        else:
            # messages.error(request, 'Verifique os erros abaixo.')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = RegisterForm()

    return render(request, 'accounts/customer_register.html', {'form': form})
                            

def customer_login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                if user.has_perm('core.view_customer_dashboard') and user.is_active:
                    auth_login(request, user)
                
                    if 'cart' in request.session:
                        Cart(request)._save_cart_to_db()

                    return redirect('home')
                else:
                    messages.error(request, 'Você não tem acesso. Registre-se.')
                    # return redirect('customer_register')
            else:
                messages.error(request, 'Credenciais inválidas. Tente novamente.')
    else:
        form = LoginForm()
    return render(request, 'accounts/customer_login.html', {'form': form})

