from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:dish_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/increase/<int:dish_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:dish_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    path('register/', views.register, name='register'),
    path(
    'login/',
    auth_views.LoginView.as_view(template_name='restaurant/login.html'),
    name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]

