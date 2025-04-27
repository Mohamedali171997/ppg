from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart, name='cart'),
    path('orders/', views.orders, name='orders'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('product/<pk>/', views.product_detail, name='product_detail'),
    path('signup/', views.signup, name='signup'),
    path('update_item/', views.updateItem, name='update_item'),
    path('header1/', views.header1, name='header1'),
    path('header2/', views.header2, name='header2'),
]
