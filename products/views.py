from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Cart, CartItem, Order, OrderItem
from .models import Product



def home(request):
    # Get all products, ordered by newest first
    products = Product.objects.all().order_by('-id')
    
    # Debug: Print to console to verify
    print(f"Found {products.count()} products")
    for p in products:
        print(f"  - {p.name}: ${p.price}")
    
    return render(request, 'products/index.html', {'products': products})

@login_required(login_url='/accounts/login/')
def cart(request):
    """Display cart - REQUIRES LOGIN"""
    cart_obj, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart_obj)
    total = sum(item.total_price() for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'products/cart.html', context)


@login_required(login_url='/accounts/login/')
def add_to_cart(request, product_id):
    """Add to cart - REQUIRES LOGIN"""
    product = get_object_or_404(Product, id=product_id)
    cart_obj, created = Cart.objects.get_or_create(user=request.user)
    
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


@login_required(login_url='/accounts/login/')
def remove_from_cart(request, item_id):
    """Remove from cart"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed!")
    return redirect('cart')


@login_required(login_url='/accounts/login/')
def update_cart(request, item_id):
    """Update cart"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
    
    return redirect('cart')


@login_required(login_url='/accounts/login/')
def checkout(request):
    """Checkout - REQUIRES LOGIN"""
    
    # DEBUG - Check console output (you can remove this later)
    print(f"User: {request.user}")
    print(f"Is Authenticated: {request.user.is_authenticated}")
    
    cart_obj, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart_obj)
    
    if not cart_items:
        messages.error(request, "Your cart is empty!")
        return redirect('cart')
    
    total = sum(item.total_price() for item in cart_items)
    
    # MAKE SURE THIS RETURN STATEMENT IS HERE!
    return render(request, 'products/checkout.html', {
        'cart_items': cart_items,
        'total': total,
    })
# @login_required(login_url='/accounts/login/')
# def checkout(request):
#     # DEBUG - Check console output
#     print(f"User: {request.user}")
#     print(f"Is Authenticated: {request.user.is_authenticated}")
    


@login_required(login_url='/accounts/login/')
def process_checkout(request):
    """Process checkout - REQUIRES LOGIN"""
    if request.method != 'POST':
        return redirect('checkout')
    
    cart_obj, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart_obj)
    
    if not cart_items:
        messages.error(request, "Your cart is empty!")
        return redirect('cart')
    
    # Get form data
    full_name = request.POST.get('full_name')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    address = request.POST.get('address')
    city = request.POST.get('city')
    postal_code = request.POST.get('postal_code')
    country = request.POST.get('country')
    
    if not all([full_name, email, phone, address, city, postal_code, country]):
        messages.error(request, "Please fill in all fields!")
        return redirect('checkout')
    
    total = sum(item.total_price() for item in cart_items)
    
    order = Order.objects.create(
        user=request.user,
        total_amount=total,
        full_name=full_name,
        email=email,
        phone=phone,
        address=address,
        city=city,
        postal_code=postal_code,
        country=country
    )
    
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )
    
    cart_items.delete()
    
    messages.success(request, f"Order #{order.id} placed successfully!")
    return redirect('order_confirmation', order_id=order.id)


@login_required(login_url='/accounts/login/')
def order_confirmation(request, order_id):
    """Order confirmation - REQUIRES LOGIN"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'products/order_confirmation.html', {'order': order})