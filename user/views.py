from django.conf.global_settings import DEFAULT_FROM_EMAIL
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.forms.utils import ErrorList
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

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
            get_name_by_email = user.email.split('@')[0]
            user.is_staff = True
            user.is_superuser = True
            user.set_password(user.password)
            user.save()
            send_mail(
                f'{get_name_by_email}',
                'You successfully registered',
                DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False
            )
            login(request, user)
            return redirect('eccomerce:index')
    context = {
        'form': form
    }

    return render(request, 'ecomerce/register.html', context=context)


class RegisterPage(RegisterForm):
    template_name = 'user/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('shop:products')

    def __init__(
            self,
            data=None,
            files=None,
            auto_id="id_%s",
            prefix=None,
            initial=None,
            error_class=ErrorList,
            label_suffix=None,
            empty_permitted=False,
            instance=None,
            use_required_attribute=None,
            renderer=None,
    ):
        super().__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, instance,
                         use_required_attribute, renderer)
        self.request = None

    def form_valid(self, form):
        user = form.save(commit=False)
        get_name_by_email = user.email.split('@')[0]
        user.is_staff = True
        user.is_superuser = True
        user.set_password(user.password)
        user.save()
        send_mail(
            f'{get_name_by_email}',
            'You successfully registered',
            DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False
        )
        login(self.request, user)
        return redirect(self.success_url)

    def form_invalid(self, form):
        pass