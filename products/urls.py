from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),
    
    # Checkout URLs
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/process/', views.process_checkout, name='process_checkout'),
    path('order/confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    # In products/urls.py
    path('order/success/<int:order_id>/', views.payment_success, name='payment_success'),
]