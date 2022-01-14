from django.shortcuts import render, redirect, HttpResponse
from app.email_backend import EmailBackend
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def login_user(request):
    return render(request, 'accounts/login.html')


def doLogin(request):
    if request.method == 'POST':
        user = EmailBackend.authenticate(request, 
            username=request.POST.get('email'),
            password=request.POST.get('password'),
        )
        if user != None:
            login(request, user)
            user_type = user.user_type
            if user_type == '1':
                return redirect('app:home')
            elif user_type == '2':
                return HttpResponse('This is Staff Panel')
            elif user_type == '3':
                return HttpResponse('This is Student Panel')
            else:
                # message
                messages.error(request, 'Email or password are invalid!')
                return redirect('accounts:login')
        else:
            # message
            messages.error(request, 'Email or password are invalid!')
            return redirect('accounts:login')


def doLogout(request):
    logout(request)
    return redirect('accounts:login')