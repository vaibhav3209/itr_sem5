from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

from django.contrib.auth.hashers import make_password, check_password


class Component(models.Model):
    CATEGORY_CHOICES = [
        ('Microcontrollers / Boards', 'Microcontrollers / Boards'),          #right wala
        ('Sensors', 'Sensors'),
        ('Actuators', 'Actuators'),
        ('Electric Components', 'Electric Components'),
        ('Displays', 'Displays'),
        ('Miscellaneous', 'Miscellaneous'),
    ]

    COMPONENT_STATUS = [
        ('Defective','Defective'),
        ('Deleted', 'Deleted'),
        ("working",'working')
    ]

    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    date_of_purchase = models.DateField()  # Optional: remove auto_now_add if you want to enter manually
    componentstatus = models.CharField(max_length=20,choices=COMPONENT_STATUS,default="working")


    @property

    
    def status(self):
        return "Empty" if self.quantity == 0 else "Present"

    def __str__(self):
        return f"{self.name} ({self.category})"

# commented by vaibhav m. on 14jan

# class IssueRecord(models.Model):
#     student_name = models.CharField(max_length=100)  #  ForeignKey to a User model
#     component = models.ForeignKey(Component, on_delete=models.CASCADE)
#     issue_date = models.DateField(auto_now_add=True)
#     return_date = models.DateField(null=True, blank=True)  # can be updated later
#
#     #to be done by vaibhav g.
#     #add 2 status columns ,change student_name to bid email data from student table usse bid aajaye
#     #dynamic cloumns
#
#     @property
#     def status(self):
#         if self.return_date:
#             return f"Returned on {self.return_date.strftime('%Y-%m-%d')}"
#         return "Not Returned"
#
#     def __str__(self):
#         return f"{self.component.name} issued to {self.student_name}"
#

class Student(models.Model):
    full_name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=50, unique=True)
    college_email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=15)
    password = models.CharField(max_length=128) 
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
     return f"{self.full_name} ({self.roll_number})"
