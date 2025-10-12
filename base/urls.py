from django.urls import path, include
from . import views


# app_name = "base"
urlpatterns = [
    path('login/', views.loginpage, name="login"),
    path('', views.home, name="home"),
    path('login/studentdash/', views.studentdashboard, name="studentdash"),
    path('login/admindash/', views.admindashboard, name="admindash"),
    path('student_reg/', views.student_reg, name="student_reg"),
    path('logout/', views.student_logout, name='logout'),
    path('student_dash/', include(('student_dash.urls', 'dash'), namespace='dash')),
    
   
] 
