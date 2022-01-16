from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages


@login_required(login_url='accounts:login')
def home(request):
    return render(request, 'app/hod/home.html', {})


@login_required(login_url='accounts:login')
def add_student(request):
    course = Course.objects.all()
    session_year = Session_Year.objects.all()
    
    if request.method == 'POST':
        profile_pic      = request.FILES.get('profile_pic')
        first_name      = request.POST.get('first_name')
        last_name       = request.POST.get('last_name')
        email           = request.POST.get('email')
        username        = request.POST.get('username')
        password        = request.POST.get('password')
        address         = request.POST.get('address')
        gender          = request.POST.get('gender')
        course_id       = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')
        
        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email Already Taken!')
            return redirect('app:add-student')
        
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username Already Exists!')
            return redirect('app:add-student')
        else:
            user = CustomUser(
                first_name = first_name,
                last_name = last_name,
                username = username,
                email = email,
                profile_pic = profile_pic,
                user_type = 3,
            )
            user.set_password(password)
            user.save()
            
            try:
                course = Course.objects.get(id=course_id)
                print(course)
            except:
                return None
            session_year = Session_Year.objects.get(id=session_year_id)
            
            student = Student(
                admin = user,
                address = address,
                session_year_id = session_year,
                course_id = course,
                gender = gender,
            )
            student.save()
            messages.success(request, user.first_name + ' ' + user.last_name + ' Is Successfully Added!')
            return redirect('app:add-student')
            
    
    context = {
        'course' : course,
        'session_year' : session_year,
    }
    
    return render(request, 'app/hod/add_student.html', context)


def view_student(request):
    student = Student.objects.all()
    
    context = {
        'student' : student,
    }
    return render(request, 'app/hod/view_student.html', context)



def edit_student(request, id):
    student = Student.objects.filter(id=id)
    course = Course.objects.all()
    session_year = Session_Year.objects.all()
    
    context = {
        'student' : student,
        'course' : course,
        'session_year' : session_year,
    }
    return render(request, 'app/hod/edit_student.html', context)


def update_student(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')
        
        user = CustomUser.objects.get(id=student_id)
        user.profile_pic = profile_pic
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username
        
        if password != None and password != '':
            user.set_password(password)
        if profile_pic != None and profile_pic != '':
            user.profile_pic = profile_pic    
        user.save()
        
        student = Student.objects.get(admin=student_id)
        student.address = address
        student.gender = gender
        
        course = Course.objects.get(id=course_id)
        student.course_id = course
        
        session_year = Session_Year.objects.get(id=session_year_id)
        student.session_year_id = session_year
        
        student.save()
        messages.success(request, 'Records Are Successfully Updated!')
        return redirect('app:view-student')
        
    return render(request, 'app/hod/edit_student.html', {})
