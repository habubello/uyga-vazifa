from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from user.forms import LoginForm, RegisterForm


def login_page(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('eccomerce:index')
            else:
                messages.add_message(request,
                                     messages.ERROR,
                                     'Notogri login')
    context = {
        'form': form
    }
    return render(request, 'login.html', context=context)

def logout_page(request):
    logout(request)
    return redirect('eccomerce:index')


def register_page(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.is_superuser = True
            user.set_password(user.password)
            user.save()
            # login(request, form)
            return redirect('eccomerce:index')
    context = {
        'form': form
    }

    return render(request, 'ecomerce/register.html', context=context)