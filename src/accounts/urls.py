from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('', views.login_user, name='login'),
    path('doLogin/', views.doLogin, name='doLogin'),
    path('doLogout/', views.doLogout, name='logout'),
]
