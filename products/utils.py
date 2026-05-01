# # products/utils.py

# from django.core.mail import send_mail, mail_admins
# from django.conf import settings


# def send_order_confirmation_email(order):
#     """
#     Send order confirmation email to customer
#     """
#     subject = f'Order Confirmation #{order.id} - MiniStore'
    
#     # Build email message
#     message = f"""
# Dear {order.full_name},

# Thank you for your order! Here are your order details:

# Order Number: #{order.id}
# Order Date: {order.created_at.strftime('%B %d, %Y')}
# Total Amount: ${order.total_amount}
# Status: {order.get_status_display()}

# Shipping Address:
# {order.full_name}
# {order.address}
# {order.city}, {order.postal_code}
# {order.country}
# Phone: {order.phone}

# Items Ordered:
# """
    
#     # Add items to email
#     for item in order.items.all():
#         message += f"\n- {item.product.name} x {item.quantity} = ${item.total_price()}"
    
#     message += f"""

# Total: ${order.total_amount}

# We'll notify you when your order ships.

# Thank you for shopping with MiniStore!
# """
    
#     # Send to customer
#     send_mail(
#         subject=subject,
#         message=message,
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         recipient_list=[order.email],
#         fail_silently=False,
#     )
    
#     return True


# def send_admin_order_notification(order):
#     """
#     Send email notification to admin when new order is placed
#     """
#     subject = f'New Order #{order.id} - ${order.total_amount}'
    
#     message = f"""
# A new order has been placed!

# Order Details:
# - Order ID: #{order.id}
# - Customer: {order.full_name}
# - Email: {order.email}
# - Phone: {order.phone}
# - Total: ${order.total_amount}
# - Status: {order.get_status_display()}

# Shipping Address:
# {order.address}, {order.city}, {order.postal_code}, {order.country}

# Items:
# """
    
#     for item in order.items.all():
#         message += f"\n- {item.product.name} x {item.quantity} = ${item.total_price()}"
    
#     # Send to admin
#     mail_admins(
#         subject=subject,
#         message=message,
#         fail_silently=False,
#     )
    
#     return True