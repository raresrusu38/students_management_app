from django.urls import path
from . import views
from app import hod_views, staff_views, student_views 

app_name = "app"

urlpatterns = [
    path('hod/home/', hod_views.home, name='home'),
]