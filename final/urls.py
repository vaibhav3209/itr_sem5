from django.urls import path
from . import views


# note:::  har url mein hyphen(-) hai and usi jagah par views mein undercore hai
#          for better url design

#yha par str:category not allow 'micro / boards' ye
# slash lagane k liye '<path:category_key>'


#note: url == admin/  will point to django admin to usko alag hi rakhna
# ab sabko url == teacher/ kardo
app_name = "final"
urlpatterns = [
    path('', views.home, name='home'),

    #login/logout urls
    path('login/', views.user_login, name="login"),
    path('student/', views.student_dashboard, name="student_dashboard"),
    path('teacher/dashboard/', views.admin_dashboard, name="admin_dashboard"),
    path('teacher/logout/', views.admin_logout, name='admin_logout'),
    path('student/logout/', views.student_logout, name='student_logout'),


    # student k baad wale path
path('student/issued_items/', views.issued_items, name="issued_items"),
path('student/request-components/', views.request_components, name="request_components"),
path('student/request-components/<path:category_key>/', views.category_items,name='category_items'),
path('student/submit_request/', views.submit_request, name='submit_request'),


    # admin k baad wale path
    # path("teacher/approved-requests/",views.approved_requests,name="approved_requests"),
    # path("teacher/rejected-requests/",views.rejected_requests,name="rejected_requests"),
    path('teacher/inventory/', views.inventory, name='inventory'),
    path('teacher/inventory/<path:category_key>/', views.inventory_items, name='inventory_items'),
    path('teacher/update-status/', views.update_status, name='update_status'),
    path('teacher/delete_component/', views.delete_component, name ='delete_component')



]