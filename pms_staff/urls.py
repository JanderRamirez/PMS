from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index, name='welcome'),
    path('profile', views.profile, name='welcome'),
    path('update_profile', views.update_profile, name='welcome'),
    path('sales', views.sales, name='welcome'),
    path('daily', views.daily_sales, name='welcome'),
    path('add_sale', views.add_sale, name='welcome'),
    path('get_detail/<str:id>',views.get_detail, name='welcome'),
    path('delete_sale/<int:id>',views.delete_sale, name='welcome'),
    path('submit_sale/<int:id>',views.submit_sale, name='welcome'),
]