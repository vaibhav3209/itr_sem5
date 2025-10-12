from django.contrib import  messages
from django.http import HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .decorators import student_login_required
from django.contrib.auth.hashers import make_password, check_password
from .models import Student , Component


def loginpage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            student = Student.objects.get(college_email=email)
        except Student.DoesNotExist:
            messages.error(request, "Student does not exist.")
            return render(request, 'base/login_register.html')

        if check_password(password, student.password):
            request.session['student_id'] = student.id  # custom session
            # return redirect('studentdash')
            return render(request,'base/studentdashboard.html',{'student':student})
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'base/login_register.html')

def home(request):
    return render(request, 'base/home.html')


def student_reg(request):
    if request.method == 'POST' and request.POST.get('form_type') == 'signup':
        email = request.POST.get('College_Email')
        password = request.POST.get('password')
        student_name = request.POST.get('Full_Name')
        roll_no = request.POST.get('Roll_Number')
        contact_number = request.POST.get('Contact_Number')

        if not all([email, password, student_name, roll_no, contact_number]):
            messages.error(request, "Please fill all the fields.")
            return render(request, 'base/login_register.html')

        if Student.objects.filter(college_email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'base/login_register.html')

        student = Student(
            full_name=student_name,
            roll_number=roll_no,
            college_email=email,
            contact_number=contact_number,
        )
        student.set_password(password)
        student.save()
        messages.success(request, "Registration successful.")
        return redirect('login')

    return render(request, 'base/login_register.html')


@student_login_required
def studentdashboard(request):
    student_id = request.session.get('student_id')
    if not student_id:
        # If session expired or not logged in, redirect to login
        return redirect('login')

    # Fetch the student object from the database
    student = Student.objects.get(id=student_id)
    return render(request, 'base/studentdashboard.html',
                  {'student':student})


def admindashboard(request):
#     if request.method == 'POST':
        return render(request, 'base/admin-dashboard.html')
#     return HttpResponse("not a post emthi from admin")


def student_logout(request):
    request.session.flush()
    return redirect('login')

