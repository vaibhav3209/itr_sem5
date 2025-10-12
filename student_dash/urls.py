from django.urls import path
from . import views

app_name = 'dash'
urlpatterns = [
    path('request/', views.inventory_request, name='inventory_request'),
    path('login/studentdash/components', views.components, name="components"),
    path('category/<path:category_key>/', views.category_items, name='category_items'),
    path('submit-request/', views.submit_request, name='submit_request'),
    path("issues/<str:roll_number>/", views.student_issues, name="student_issues"),
    path('admindash/', views.admindashboard, name="admindash"),
    path("admindash/approved/",views.approved_requests,name="approved_requests"),
    path('return-status/', views.return_status, name='return_status'),
    path("admindash/rejected/",views.rejected_requests,name="rejected_requests"),
    path('update-status/', views.update_status, name='update_status'),
    path('admindash/inventory/', views.change_inventory, name='inventory_page'),

                                          #yha par str:category not allow 'micro / boards' ye
                                           # slash lagane k liye 'path:category_key'
    path('admindash/inventory/category/<path:category_key>/', views.inv_items, name='inv_items'),
    path('delete-component/', views.delete_component, name='deletecomp'),

    path("add_component/", views.add_component, name="add_component"),

path('logout/', views.teacher_logout, name='logout'),
   



]