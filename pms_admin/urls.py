from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='welcome'),
    path('profile', views.profile, name='welcome'),
    path('update_profile', views.update_profile, name='welcome'),
    
    path('medicine', views.medicine, name='welcome'),
    path('add_med', views.add_med, name='welcome'),
    path('edit_med', views.edit_med, name='welcome'),
    path('add_stock', views.add_stock, name='welcome'),
    path('get_med/<int:id>', views.get_med, name='welcome'),

    path('category', views.category, name='welcome'),
    path('add_cat', views.add_cat, name='welcome'),
    path('get_cat/<int:id>', views.get_cat, name='welcome'),
    path('edit_cat', views.edit_cat, name='welcome'),

    path('cashier', views.cashier, name='welcome'),
    path('add_cas', views.add_cas, name='welcome'),
    path('get_cas/<int:id>', views.get_cas, name='welcome'),
    path('edit_cas', views.edit_cas, name='welcome'),

    path('sales', views.sales, name='welcome'),
    path('get_sales/<int:id>', views.get_sales, name='welcome'),
    path('get_monthly', views.get_monthly, name='welcome'),
    path('get_bymed', views.get_bymed, name='welcome'),
]