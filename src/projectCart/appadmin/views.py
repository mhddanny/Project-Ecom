from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader

from accounts.models import UserProfile
from store.models import Product

from . forms import UserForm, UserProfileForm
from . forms import UserProductForm


@login_required
def dashboard_admin(request):
    return render (request, 'appadmin/dashboard.html')

@login_required
def orders(request):
    return render(request, 'appadmin/orders/index.html')


@login_required
def products(request):
    context = {}
    products = Product.objects.all().filter(is_available=True).order_by('id')
    paginator = Paginator(products, 10)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = products.count()
    
    context = {'products': paged_products, 'product_count': product_count}
        
    return render(request, 'appadmin/product/index.html', context)

@login_required
def add_product(request):
    product_form = UserProductForm()

    context = {
        'product': product_form
    }
    return render(request, 'appadmin/product/add_product.html', context)

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
