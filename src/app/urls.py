from django.urls import path
from . import views
from app import hod_views, staff_views, student_views 

app_name = "app"

urlpatterns = [
    path('', hod_views.home, name='home'),
    path('hod/student/add/', hod_views.add_student, name='add-student'),
    path('hod/student/view/', hod_views.view_student, name='view-student'),
    path('hod/student/edit/<int:id>/', hod_views.edit_student, name='edit-student'),
    path('hod/student/update/', hod_views.update_student, name='update-student'),
]