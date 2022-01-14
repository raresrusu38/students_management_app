from django.urls import path
from . import views, hod_views, staff_views, student_views

app_name = "app"

urlpatterns = [
    path('', views.index, name='home'),
]