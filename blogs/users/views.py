from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import login, authenticate



def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user_details')
    else:
        form = UserRegistrationForm()
    return render(request, 'register_step1.html', {'form': form})

def user_details(request):
    if request.method == 'POST':
        form = UserDetailsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('blog_list')
    else:
        form = UserDetailsForm(instance=request.user)
    return render(request, 'register_step2.html', {'form': form})
        
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('blog_list')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})
