from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path
from Ecommerce import views # Import your views from the Ecommerce app
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart, name='cart'),
    path('orders/', views.orders, name='orders'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('product/<pk>/', views.product_detail, name='product_detail'),
    path('signup/', views.signup, name='signup'),
    path('update_item/', views.update_item, name='update_item'),
    path('header1/', views.header1, name='header1'),
    path('header2/', views.header2, name='header2'),
    path('cart/update_item/', views.update_item, name='update_item'),
    #stripe payment
path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
   # path('success/', views.payment_success, name='payment_success'),
   # path('cancel/', views.payment_cancel, name='payment_cancel'),
    # NEW: URL for the Gemini Assistant
    path('gemini-assistant/', views.gemini_chat_view, name='gemini_assistant'),

]
