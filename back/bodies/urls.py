from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path("", views.product_list, name='product_list'),
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name = "./login.html"), name='login'),
    path("logout/", auth_views.LogoutView.as_view(), name='logout'),
    path("orders/", views.order_list, name='order_list'),
    path("buy/<int:product_id>&<int:pickup_point_id>", views.create_order, name='create_order'),

    
]
