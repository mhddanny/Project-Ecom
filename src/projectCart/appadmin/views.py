from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import UserProfile

from . forms import UserForm, UserProfileForm


@login_required
def dashboard_admin(request):
    return render (request, 'admin/dashboard.html')

@login_required
def customer(request):
    return render (request, 'admin/product/index.html')

@login_required
def product(request):
    return render (request, 'admin/product/index.html')

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
            return redirect('profile_admin')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile
    }
    return render (request, 'admin/profile/profile_edit.html', context)

