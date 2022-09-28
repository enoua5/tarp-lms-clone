from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.contrib import messages
from .forms import RegistrationForm
from account.models import Profile
from django.contrib.auth.models import Group
from django.contrib.auth.models import User


def login(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        return render(request, 'authentication/login.html', {'form':form})
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                user = User.objects.get(username=username)
                return redirect('dashboard:dashboard')
                # User not found
        else:
            # If there were errors, we render the form with these
            # errors
            return render(request, 'authentication/login.html', {'form': form}) 


def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            # log new user in
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            new_user = auth.authenticate(username=username, password=password)
            auth.login(request, new_user)

            # create profile record for new user
            new_user_profile = Profile(user=new_user, birthdate=form.cleaned_data.get('birthdate'))
            new_user_profile.save()

            # Get the group name from the form
            groupname = form.cleaned_data.get('account_type')

            # Get our group with a selected name
            ourGroups = Group.objects.get(name=(groupname))

            # Get the user with the found username
            user = User.objects.get(username=username)

            # Push the user into an appropriate group!
            ourGroups.user_set.add(user)

            return redirect('dashboard:dashboard')
    else:
        form = RegistrationForm()

    args = {}
    args['form'] = form
    return render(request, 'authentication/signup.html', args)
