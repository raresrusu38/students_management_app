from django.shortcuts import render, redirect, HttpResponse
from app.email_backend import EmailBackend
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.models import CustomUser
from django.shortcuts import get_object_or_404

# Create your views here.

def login_user(request):
    return render(request, 'accounts/login.html')


def doLogin(request):
    if request.method == 'POST':
        user = EmailBackend.authenticate(request, 
            username=request.POST.get('username'),
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


@login_required(login_url='/accounts/login/')
def profile(request):
    try:
        user = CustomUser.objects.get(id__exact=request.user.id)
        print(user)
    except:
        user = None
        print(user, 'None')
    
    context = {
        'user' : user,
    }
    
    return render(request, 'accounts/profile.html', context)


@login_required(login_url='/accounts/login/')
def profile_update(request):
    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        first_name  = request.POST.get('first_name')
        last_name   = request.POST.get('last_name')
        # username    = request.POST.get('username')
        # email       = request.POST.get('email')
        password    = request.POST.get('password')
        
        try:
            custom_user = CustomUser.objects.get(id=request.user.id)
            
            custom_user.first_name  = first_name
            custom_user.last_name   = last_name
            custom_user.profile_pic = profile_pic
           
            if password != None and password != "":
                custom_user.set_password(password)
               
            if profile_pic != None and profile_pic != "":
                custom_user.profile_pic = profile_pic
            
            custom_user.save()
            messages.success(request, 'Your Profile Updated Successfully!')
            return redirect('accounts:profile')
        except:
            messages.error(request, 'Failed To Update Your Profile!')
        
    return render(request, 'accounts/profile.html')
