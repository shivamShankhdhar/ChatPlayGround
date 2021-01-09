from accounts.forms import AccountAuthenticationForm, RegistrationForm
from django.shortcuts import render, redirect

from django.http import HttpResponse

from django.contrib.auth import login, authenticate, logout

def register_view(request, *args, **kwargs):
    template_name = 'accounts/register.html'
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f"You are already authenticated as {user.email}.")
        
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # after registerration user will automatic login 
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email = email, password = raw_password)
            login(request, account)
            destination = get_redirect_if_exists(request)
            if destination:
                return redirect(destination)
            return redirect("home")

        else:
            context['registration_form'] = form

    return render(request, template_name, context )


def logout_view(request):
    logout(request)
    return redirect('home')

def login_view(request, *args, **kwargs):
    template_name = 'accounts/login.html'
    context = {}

    if request.user.is_authenticated:
        return redirect('home')
    
    destination = get_redirect_if_exists(request)
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email = email, password = password)
            if user:
                login(request, user)
                destination = get_redirect_if_exists(request)
                if destination:
                    return redirect(destination)
                return redirect('home')
        else:
            context['login_form'] = form

    return render(request, template_name, context)

def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.Get.get("next"):
            redirect = str(request.GET.get('next'))
