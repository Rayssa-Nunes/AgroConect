from django.urls import path

from . import views

urlpatterns = [
    path('fair/', views.fair_view, name='fair'),
    path('fair_list/', views.fair_list, name='fair_list'),
    path('leave_fair/<id>', views.leave_fair, name='leave_fair'),
]
