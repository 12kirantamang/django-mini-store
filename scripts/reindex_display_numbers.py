from products.models import Product

for idx, p in enumerate(Product.objects.order_by('id'), start=1):
    p.display_number = idx
    p.save(update_fields=['display_number'])

print('Reindexed', Product.objects.count(), 'products')
