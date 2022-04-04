from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

from account.forms import RegistrationForm, LoginForm

# Create your views here.

def profile_view(request, *args, **kwargs):
    user_ip = request.META.get('REMOTE_ADDR')

    context = {
        'user_ip': user_ip
    } 
    return render(request,'account/profile.html',context)
    
def logout_view(request, *args, **kwargs):
    logout(request)
    messages.success(request,'You have been logged out.')
    return redirect("home_view")


def login_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect("home_view")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password")
            user = authenticate(email=email, password=raw_password)
            if user:
                login(request, user)  # Login the user
                messages.success(request,"Logged in successfully.")
                return redirect("home_view")
            else:
                messages.error(request,"Invalid Login.")
                form = LoginForm() 

    else:
        form = LoginForm()

    context = {"form": form}
    return render(request, "account/login.html", context)


def register_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect("home_view")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Create the account
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password1")
            account = authenticate(email=email, password=raw_password)
            login(request, account)  # Login the user
            messages.success(
                request, f'Account created for {form.cleaned_data.get("email")}.'
            )
            return redirect("home_view")
    else:
        form = RegistrationForm()

    context = {"form": form}

    return render(request, "account/register.html", context)
