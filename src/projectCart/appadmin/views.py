from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.utils.text import slugify

from accounts.models import UserProfile
from store.models import Product, ProductPaket, ProductGallery
from category.models import Category

from django.forms import modelformset_factory

from . forms import UserForm, UserProfileForm
from . forms import UserProductForm, UserProductPaketForm, UserProductGaleryForm, UserCategoryForm


@login_required
def dashboard_admin(request):
    return render (request, 'appadmin/dashboard.html')

@login_required
def orders(request):
    return render(request, 'appadmin/orders/index.html')

@login_required
def category(request):
    # context = {}
    category = Category.objects.order_by('category_name')
    paginator = Paginator(category,5)
    page = request.GET.get('page')
    paged_category = paginator.get_page(page)
    category_count = category.count()
    print(category)

    template = loader.get_template("appadmin/category/index.html")
    context = {'category': paged_category, 'category_count': category_count}
    return HttpResponse(template.render(context, request))

def add_category(request):

    category_form = UserCategoryForm()

    context = {
        'title': 'Edit',
        'category': category_form,
    }
    return render(request, "appadmin/category/set_category.html", context)

@login_required
def edit_category(request, slug, pk):
    try:
        category_get = get_object_or_404(Category, pk=pk)


        category_form = UserCategoryForm(instance=category_get)

    except Category.DoesNotExist:
        raise Http404("Product Tidak di temukan")

    context = {
        'title': 'Edit',
        'category': category_form,
    }
    return render(request, "appadmin/category/set_category.html", context)


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
        product_images = request.FILES.getlist("image")
        
        if product_form.is_valid() and paket_form.is_valid():
            product_name = request.POST.get('product_name')
            product = product_form.save(commit=False)
            product.slug = slugify(product_name)
            # print(product.id)
            paket = paket_form.save(commit=False) 
            paket.product = product
            product.save()
            paket.save()
            for i in product_images:
                ProductGallery.objects.create(product=product, image=i)

            messages.success(request, 'Product has been succesfuly')
            return redirect('products')
        else:
            print(product_form.errors and paket_form.errors )
    else:
        product_form = UserProductForm()
        paket_form = UserProductPaketForm()
        product_images = UserProductGaleryForm()

    context = {
        'title': 'Add',
        'product': product_form,
        'paket': paket_form,
        'product_images': product_images,
    }
    return render(request, 'appadmin/product/add_product.html', context)

@login_required
def edit_product(request, pk):
    product_get = get_object_or_404(Product, pk=pk)
    product_paket = ProductPaket.objects.get(product=product_get)
    ImagesFormSet = modelformset_factory(ProductGallery, form=UserProductGaleryForm, extra=2, max_num=7)
    
    if request.method == 'POST':
        product_form = UserProductForm(request.POST, request.FILES, instance=product_get)
        paket_form = UserProductPaketForm(request.POST, instance=product_paket)   
        product_images = ImagesFormSet(request.POST or None, request.FILES or None)
        
        if product_form.is_valid() and paket_form.is_valid() and product_images.is_valid():
            product_name = product_form.cleaned_data['product_name']
            product = product_form.save(commit=False)
            product.slug = slugify(product_name)
            product.save()
            paket_form.save()

            print(product_images.cleaned_data)
            # data = ProductGallery.objects.get(product=product_get)
            # for index, i in enumerate(product_images):
            #     if i.cleaned_data:
            #         if i.cleaned_data['id'] is None:
            #             photo = ProductGallery(product=product_get, image=i.cleaned_data.get['image'])
            #             photo.save()
            #         else:
            #             photo = ProductGallery(product=product_get, image=i.cleaned_data.get['image'])
            #             d = ProductGallery.objects.get(id=data[index].id)
            #             d.image = photo.image
            #             d.save()

            messages.success(request, 'Change has been succesfuly')
            return redirect('products')
    else:
        product_form = UserProductForm(instance=product_get)
        paket_form = UserProductPaketForm(instance=product_paket)
        product_images = ImagesFormSet(queryset=ProductGallery.objects.filter(product=product_get))

    context = {
        'title': 'Edit',
        'product': product_form,
        'paket': paket_form,
        'product_images': product_images,
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
