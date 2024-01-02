from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.utils.text import slugify

from accounts.models import UserProfile
from store.models import Product, ProductPaket
from category.models import Category

from . forms import UserForm, UserProfileForm
from . forms import UserProductForm, UserProductPaketForm


@login_required
def dashboard_admin(request):
    return render (request, 'appadmin/dashboard.html')

@login_required
def orders(request):
    return render(request, 'appadmin/orders/index.html')

@login_required
def category(request):
    # context = {}
    category = Category.objects.all().order_by('category_name')
    paginator = Paginator(category, 10)
    page = request.GET.get('page')
    paged_category = paginator.get_page(page)
    category_count = category.count()
    print(category)
    
    context = {'category': category, 'category_count': category_count}
    return render(request, 'appadmin/category/index.html')

@login_required
def products(request):
    context = {}
    products = Product.objects.all().filter(is_available=True).order_by('-created_date')
    paginator = Paginator(products, 10)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = products.count()
    
    context = {'products': paged_products, 'product_count': product_count}
        
    return render(request, 'appadmin/product/index.html', context)

@login_required
def add_product(request):
    if request.method == 'POST':
        product_form = UserProductForm(request.POST, request.FILES)
        paket_form = UserProductPaketForm(request.POST) 
        if product_form.is_valid() and paket_form.is_valid():
            product_name = request.POST.get('product_name')
            product = product_form.save(commit=False)
            product.slug = slugify(product_name)
            # print(product.id)
            paket = paket_form.save(commit=False) 
            paket.product = product
            product.save()
            paket.save()

            messages.success(request, 'Product has been succesfuly')
            return redirect('products')
    else:
        product_form = UserProductForm()
        paket_form = UserProductPaketForm()

    context = {
        'title': 'Add',
        'product': product_form,
        'paket': paket_form
    }
    return render(request, 'appadmin/product/add_product.html', context)

@login_required
def edit_product(request, pk):
    product_get = get_object_or_404(Product, pk=pk)
    product_paket = ProductPaket.objects.get(product=product_get)
    
    if request.method == 'POST':
        product_form = UserProductForm(request.POST, request.FILES, instance=product_get)
        paket_form = UserProductPaketForm(request.POST, instance=product_paket)   
        if product_form.is_valid() and paket_form.is_valid():
            product_form.save()
            paket_form.save()

            messages.success(request, 'Change has been succesfuly')
            return redirect('products')
    else:
        product_form = UserProductForm(instance=product_get)
        paket_form = UserProductPaketForm(instance=product_paket)

    context = {
        'title': 'Edit',
        'product': product_form,
        'paket': paket_form
    }
    return render(request, 'appadmin/product/add_product.html', context)

@login_required
def delete_product(request, pk):
    product = Product.objects.get(pk=pk)
    # paket = ProductPaket.objects.get(product=product).delete()
    product.delete()

    messages.success(request, 'Deleted was susccesfully')
    return redirect('products')

@login_required
def profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been update')
            return redirect('profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile
    }
    return render (request, 'appadmin/profile/profile_edit.html', context)

@login_required
def customers(request):

    customer = UserProfile.objects.all().filter(user__is_admin="False", user__is_active="True")[:4]
    context = {
        'customer': customer
    }

    return render(request, 'appadmin/customer/index.html', context)
