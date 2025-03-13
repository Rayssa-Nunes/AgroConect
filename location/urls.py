from django.urls import path

from . import views

urlpatterns = [
    path('fair/', views.fair_view, name='fair'),
    path('my_fair_list/', views.my_fair_list, name='my_fair_list'),
    path('leave_fair/<id>', views.leave_fair, name='leave_fair'),
    path('fair_list/', views.fair_list, name='fair_list'),

    path('map/', views.map_view, name='map'),
]
