from django.shortcuts import render
from store.models import Product, ReviewRating

def home (request):
    products = Product.objects.all().filter(is_available=True).order_by('created_date')

    # Descending Order
    new_product = Product.objects.all().filter(is_available=True).order_by('-created_date')[:4]

    # Get The reviews
    reviews = None
    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)


    context = {
        'products': products,
        'reviews': reviews,
        'new_product': new_product 
        }
    return render(request, 'home.html', context)