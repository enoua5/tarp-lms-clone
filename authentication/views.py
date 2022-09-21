from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.contrib import messages
from .forms import RegistrationForm

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
                name = user.get_full_name()
                messages.success(request, f'Welcome {name}')
                return redirect('authentication:viewData')
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
            fName = form.cleaned_data.get('first_name')
            lName = form.cleaned_data.get('last_name')
            messages.success(request, f'Welcome {fName} {lName}!')
            return redirect('authentication:viewData')
    else:
        form = RegistrationForm()

    args = {}
    args['form'] = form
    return render(request, 'authentication/signup.html', args)
