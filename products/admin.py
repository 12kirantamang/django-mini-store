from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Cart, CartItem, Order, OrderItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'image_preview', 'description']
    list_editable = ['price']
    search_fields = ['name', 'description']
    list_filter = ['price']
    ordering = ['name']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px; object-fit: cover;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Image'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price', 'total_price', 'product_image']
    fields = ['product', 'product_image', 'quantity', 'price', 'total_price']
    can_delete = False
    
    def total_price(self, obj):
        return f"${obj.total_price()}"
    total_price.short_description = 'Total'
    
    def product_image(self, obj):
        if obj.product and obj.product.image:
            return format_html('<img src="{}" style="max-height: 40px; max-width: 40px; object-fit: cover; border-radius: 4px;" />', obj.product.image.url)
        return "No Image"
    product_image.short_description = 'Image'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_id', 
        'customer_name', 
        'email', 
        'total_amount', 
        'status',  
        'status_colored', 
        'created_at', 
        'item_count',
        'is_paid',
        'payment_method',
    ]
    list_filter = ['status', 'created_at', 'city']
    search_fields = [
        'id', 
        'full_name', 
        'email', 
        'phone', 
        'address', 
        'user__username'
    ]
    readonly_fields = [
        'id',
        'user',
        'total_amount',
        'created_at',
        'order_summary'
    ]
    inlines = [OrderItemInline]
    list_editable = ['status']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Order Information', {
            'fields': (
                'id',
                'user',
                'status',
                'is_paid', 
                'stripe_payment_intent_id',
                'total_amount',
                'created_at'
            )
        }),
        ('Customer Details', {
            'fields': (
                'full_name',
                'email',
                'phone'
            )
        }),
        ('Shipping Address', {
            'fields': (
                'address',
                'city',
                'postal_code',
                'country'
            )
        }),
        ('Order Summary', {
            'fields': ('order_summary',)
        })
    )
    
    def order_id(self, obj):
        return f"#{obj.id}"
    order_id.short_description = 'Order ID'
    order_id.admin_order_field = 'id'
    
    def customer_name(self, obj):
        return obj.full_name
    customer_name.short_description = 'Customer'
    
    def status_colored(self, obj):
        colors = {
            'pending': 'orange',
            'processing': 'blue',
            'shipped': 'purple',
            'delivered': 'green',
            'cancelled': 'red'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="color: {}; font-weight: bold; text-transform: uppercase;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_colored.short_description = 'Status'
    status_colored.admin_order_field = 'status'
    
    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Items'
    
    def order_summary(self, obj):
        items = obj.items.all()
        html = '<table style="width: 100%; border-collapse: collapse;">'
        html += '<tr style="background: #f5f5f5;">'
        html += '<th style="padding: 8px; border: 1px solid #ddd;">Product</th>'
        html += '<th style="padding: 8px; border: 1px solid #ddd;">Qty</th>'
        html += '<th style="padding: 8px; border: 1px solid #ddd;">Price</th>'
        html += '<th style="padding: 8px; border: 1px solid #ddd;">Total</th>'
        html += '</tr>'
        
        for item in items:
            html += '<tr>'
            html += f'<td style="padding: 8px; border: 1px solid #ddd;">{item.product.name}</td>'
            html += f'<td style="padding: 8px; border: 1px solid #ddd; text-align: center;">{item.quantity}</td>'
            html += f'<td style="padding: 8px; border: 1px solid #ddd;">${item.price}</td>'
            html += f'<td style="padding: 8px; border: 1px solid #ddd;">${item.total_price()}</td>'
            html += '</tr>'
        
        html += '<tr style="background: #e8f5e9; font-weight: bold;">'
        html += f'<td colspan="3" style="padding: 8px; border: 1px solid #ddd; text-align: right;">Total Amount:</td>'
        html += f'<td style="padding: 8px; border: 1px solid #ddd;">${obj.total_amount}</td>'
        html += '</tr>'
        html += '</table>'
        
        return format_html(html)
    order_summary.short_description = 'Order Items Summary'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'item_count', 'created_at']
    readonly_fields = ['user', 'created_at']
    
    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Items'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'total_price']
    list_filter = ['cart__user']
    
    def total_price(self, obj):
        return f"${obj.total_price()}"
    total_price.short_description = 'Total'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price', 'total_price']
    list_filter = ['order__status']
    search_fields = ['order__id', 'product__name']
    readonly_fields = ['order', 'product', 'quantity', 'price']
    
    def total_price(self, obj):
        return f"${obj.total_price()}"
    total_price.short_description = 'Total'