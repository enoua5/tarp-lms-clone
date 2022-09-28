from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UpdateUserForm, UpdateProfileForm
from .models import Profile


# Create your views here.
@login_required
def profile(request):

    return render(request, 'account/profile.html', {})


@login_required
def edit(request):

    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('account:profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})
