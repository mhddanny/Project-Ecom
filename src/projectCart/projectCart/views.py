from django.shortcuts import render
from store.models import Product, ReviewRating
from category.models import Category

def home (request):
    category = Category.objects.get(id=3)
    print(category)
    products = Product.objects.all().filter(is_available=True).order_by('created_date')[:6]

    # Descending Order
    new_product = Product.objects.all().filter(is_available=True).order_by('-created_date')[:3]

    # Get The reviews
    reviews = None
    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)


    context = {
        'category': category,
        'products': products,
        'reviews': reviews,
        'new_product': new_product 
        }
    return render(request, 'home.html', context)


def chat_bubble(request):
    context = {}
    return render(request, 'chat/chat_bubble.html', context)