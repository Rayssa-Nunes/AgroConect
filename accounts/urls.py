from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .forms import CustomPasswordResetForm, CustomSetPasswordForm

urlpatterns = [
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('vendor_register/', views.vendor_register_view, name='vendor_register'),
    path('vendor_login/', views.vendor_login_view, name='vendor_login'),

    path('logout/', views.logout_user, name='logout'),


    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset_form.html', form_class=CustomPasswordResetForm), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html', form_class=CustomSetPasswordForm), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),

    # path('vendor_dashboard/', views.vendor_dashboard_view, name='vendor_dashboard'),
]