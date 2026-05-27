# products/models.py

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Product(models.Model):
    CATEGORY_CHOICES = [
        # ('mobile', 'Mobile Phone'),
        # ('watch', 'Smart Watch'),
        # ('laptop', 'Laptop'),
        # ('tablet', 'Tablet'),
        ('accessory', 'Accessory'),
    ]
    
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='mobile')
    stock = models.PositiveIntegerField(default=10)
    # A human-friendly sequential number used for display (1..N).
    # Kept sequential on create and re-indexed when a product is deleted.
    display_number = models.PositiveIntegerField(null=True, blank=True, unique=True)
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Assign a sequential display_number on first save if not set.
        if not self.display_number:
            # Find current max and add 1
            max_num = Product.objects.aggregate(max_num=Max('display_number'))['max_num'] or 0
            self.display_number = max_num + 1
        super().save(*args, **kwargs)


# CART MUST COME BEFORE CARTITEM
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Cart of {self.user.username}"


# CARTITEM COMES AFTER CART
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    def total_price(self):
        return self.product.price * self.quantity


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Shipping details
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, null=True)
    is_paid = models.BooleanField(default=False) 
    payment_method = models.CharField(max_length=50, default='Stripe')
    
    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    def total_price(self):
        return self.price * self.quantity


class Wishlist(models.Model):
    """Simple wishlist: user -> product many-to-many represented as rows for easy extension."""
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='wishlists')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} wishes {self.product.name}"


@receiver(post_delete, sender=Product)
def resequence_display_numbers(sender, instance, **kwargs):
    """
    After a product is deleted, re-number remaining products so display_number
    values form a contiguous sequence starting at 1. Uses bulk update per-row
    via queryset.update() to avoid triggering save() hooks repeatedly.
    """
    # Reassign display numbers based on PK order for determinism
    products = Product.objects.order_by('id').values_list('id', flat=True)
    for idx, pk in enumerate(products, start=1):
        Product.objects.filter(pk=pk).update(display_number=idx)