import stripe
from decimal import Decimal
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.contrib.auth import logout
from .models import Product, Cart, CartItem, Order, OrderItem
from .models import Product
from django.db.models import Q

#  Stripe with the key from  settings
stripe.api_key = settings.STRIPE_SECRET_KEY

def home(request):
    """Display all products"""
    if request.user.is_authenticated and request.user.is_staff:
        logout(request)
    products = Product.objects.all().order_by('-id')
    return render(request, 'products/index.html', {'products': products})

@login_required
def cart(request):
    """Display user cart"""
    cart_obj, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart_obj)
    total = sum(item.total_price() for item in cart_items)
    return render(request, 'products/cart.html', {'cart_items': cart_items, 'total': total})

@login_required
def add_to_cart(request, product_id):
    """Add a product to the cart"""
    product = get_object_or_404(Product, id=product_id)
    cart_obj, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart_obj, 
        product=product, 
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"{product.name} added to cart!")
    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed!")
    return redirect('cart')

@login_required
def update_cart(request, item_id):
    """Change item quantity"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('cart')

@login_required
def checkout(request):
    """Show the checkout page"""
    cart_obj, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart_obj).select_related('product')
    
    if not cart_items.exists():
        messages.error(request, "Your cart is empty!")
        return redirect('cart')
    
    total = sum(item.total_price() for item in cart_items)
    return render(request, 'products/checkout.html', {
        'cart_items': cart_items,
        'total': total,
    })

@login_required
def process_checkout(request):
    """The main engine: Handles order creation and Stripe redirect"""
    if request.method != 'POST':
        return redirect('checkout')
    
    cart_obj = get_object_or_404(Cart, user=request.user)
    cart_items = cart_obj.items.all()
    
    if not cart_items.exists():
        messages.error(request, "Cart is empty!")
        return redirect('cart')

    # 1. Collect form data
    full_name = request.POST.get('full_name')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    address = request.POST.get('address')
    city = request.POST.get('city')
    postal_code = request.POST.get('postal_code')
    country = request.POST.get('country')
    selected_method = request.POST.get('payment_method', 'Stripe')

    # 2. Math & Validation
    total = sum(item.total_price() for item in cart_items)
    amount_in_cents = int(Decimal(str(total)) * 100)

    if amount_in_cents <= 0:
        messages.error(request, "Invalid order amount.")
        return redirect('cart')

    # 3. Create the Database Order
    order = Order.objects.create(
        user=request.user,
        total_amount=total,
        full_name=full_name,
        email=email,
        phone=phone,
        address=address,
        city=city,
        postal_code=postal_code,
        country=country,
        payment_method=selected_method,
        is_paid=False
    )

    # 4. Create Order Items
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

    # 5. Stripe vs COD
    if selected_method == 'Stripe':
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {'name': f"Order #{order.id}"},
                        'unit_amount': amount_in_cents,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri(f'/order/success/{order.id}/'),
                cancel_url=request.build_absolute_uri('/checkout/'),
            )
            cart_items.delete()
            return redirect(checkout_session.url)
            
        except Exception as e:
            print(f"Stripe Error: {e}")
            messages.error(request, f"Payment system error: {e}")
            return redirect('checkout')

    # Handle Cash on Delivery
    cart_items.delete()
    messages.success(request, f"Order #{order.id} placed successfully!")
    return redirect('order_confirmation', order_id=order.id)

@login_required
def payment_success(request, order_id):
    """Mark order as paid after Stripe success"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.is_paid = True
    order.save()
    return render(request, 'products/payment_success.html', {'order': order})

@login_required(login_url='/accounts/login/')
def order_confirmation(request, order_id):
    """Order confirmation - REQUIRES LOGIN"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'products/order_confirmation.html', {'order': order})


def search(request):
    query = request.GET.get('q')
    products = []

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    return render(request, 'products/search_results.html', {
        'query': query,
        'products': products
    })


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'products/product_detail.html', {
        'product': product
    })