from django.urls import path
from . import views

app_name = "final"
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name="login"),
    path('student/', views.student_dashboard, name="student_dashboard"),
    path('teacher/logout/', views.admin_logout, name='admin_logout'),
    path('student/logout/', views.student_logout, name='student_logout'),

    path('student/issued_items/', views.issued_items, name="issued_items"),
    path('student/request-components/', views.request_components, name="request_components"),
    path('student/request-components/<path:slug>/', views.category_items,name='category_items'),
    path('student/submit_request/', views.submit_request, name='submit_request'),

    path('teacher/dashboard/', views.admin_dashboard, name="admin_dashboard"),
    path('teacher/approved/', views.approved, name="approved"),
    path('teacher/inventory/', views.inventory, name='inventory'),
    path('teacher/inventory-items/<path:slug>/', views.inventory_items, name='inventory_items'),
    path('teacher/update-status/', views.update_status, name='update_status'),
    path('teacher/all-students/', views.all_students, name='all_students'),
    path('teacher/all-students/<str:id>', views.student_details, name='student_details'),

    path('teacher/delete_component/', views.delete_component, name ='delete_component')
]