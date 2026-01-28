from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import RegexValidator, EmailValidator
from django.core.exceptions import ValidationError
from django.db.models import Q

# ---------- Validators ----------
name_validator = RegexValidator(
    regex=r'^[A-Za-z]{2,30}$',
    message="Only letters allowed (2–30 characters)"
)

roll_validator = RegexValidator(
    regex=r'^[2-5][0-9][a-zA-Z]{5}[0-9]{3}$',
    message="Roll number must be exactly 10 digits"
)

phone_validator = RegexValidator(
    regex=r'^[6-9][0-9]{9}$',
    message="Enter a valid Indian mobile number"
)

college_email_validator = RegexValidator(
    regex=r'^[bB][2-5][0-9]{5}@skit\.ac\.in$',
    message="Use your official college email"
)

class ComponentCategory(models.Model):
    comp_cate_category_name = models.CharField(max_length=30)               #max 30 bytes

    def __str__(self):
        # jab ye print karte tab aise return hoga
        # cat = Category.objects.get(id=1)
        # print(cat)
        return f"{self.comp_cate_category_name}"



class Component(models.Model):
    comp_name = models.CharField(max_length=100)                            #max 100 bytes
    comp_quantity_available = models.PositiveIntegerField(default=0)          # 4 bytes
    comp_category = models.ForeignKey(ComponentCategory,on_delete=models.PROTECT,
                                      related_name="componentcategory_fkey",db_index=True)

    comp_popularity = models.PositiveIntegerField(default=0)
    comp_status = models.BooleanField(default=True)

# ***ALSO:: THIS WILL BE PRINTED IN ADMIN PANEL IF ISS MODEL KI KOI FOREGIN KEY HAI ***
    def __str__(self):
        return f"{self.comp_category.comp_cate_category_name}"


class Branches(models.Model):
    branches_branch_name =models.CharField(max_length=30)
    branches_branch_code =models.CharField(max_length=3)
    branches_rollno_code = models.CharField(max_length=3,default="CX")
    def __str__(self):
        return f"{self.branches_branch_code}"



class Student(models.Model):
    YEAR_CHOICES = [
        (1, "1st"),
        (2, "2nd"),
        (3, "3rd"),
        (4, "4th"),
        (5, "5th"),
    ]

    std_id = models.BigAutoField(primary_key=True)

    std_first_name = models.CharField(max_length=30,validators=[name_validator])
    std_last_name = models.CharField(max_length=30,validators=[name_validator])

    std_branch=models.ForeignKey(Branches,on_delete=models.PROTECT,related_name="branch_name",
                                 db_index=True,default=5)    # 5 pe IOT hai
    std_year=models.PositiveSmallIntegerField(choices=YEAR_CHOICES,db_index=True,default=2)

    std_roll_number = models.CharField(max_length=10, unique=True,validators=[roll_validator])
    std_college_email = models.EmailField(unique=True,validators=[college_email_validator])
    std_phone_number = models.CharField(max_length=10, null=True, unique=True,validators=[phone_validator])

    std_password = models.CharField(max_length=128)

    std_year_of_passing = models.PositiveSmallIntegerField(db_index=True)
    std_is_active = models.BooleanField(default=True,db_index=True)

    std_joined_at = models.DateField(auto_now_add=True)
    std_deactivated_at = models.DateField(null=True, blank=True)

    def set_password(self, raw_password):
        self.std_password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.std_password)

    @property
    def std_full_name(self):
        return f"{self.std_first_name} {self.std_last_name}"

#jab bhi save aur create call hoga tab full_clean se validate hoga pehle

    def save(self, *args, **kwargs):
        self.full_clean()  # 🚨 forces validation on save
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.std_full_name} ({self.std_roll_number}) "


    class Meta:
        constraints = [
            # Roll number: exactly 10 digits
            models.CheckConstraint(
                check=Q(std_roll_number__regex=r'^[2-5][0-9][a-zA-Z]{5}[0-9]{3}$'),
                name="roll_number_10_digits"
            ),

            # Phone number: Indian mobile format
            models.CheckConstraint(
                check=Q(std_phone_number__regex=r'^[6-9][0-9]{9}$'),
                name="phone_number_india"
            ),

            # College email domain
            models.CheckConstraint(
                check=Q(std_college_email__regex=r'^[bB][2-5][0-9]{5}@skit\.ac\.in$'),
                name="college_email_domain"
            ),

            # First and last name not same (**** LOWER CASE MEIN STORE KIYA HAI IN DATABSE ****)
            models.CheckConstraint(
                check=~Q(std_first_name=models.F('std_last_name')),
                name="first_last_name_not_same"
            ),

        ]


class StudentIssueLog(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="std_issue_logs",
        db_index=True                           #index wha pe lagana jo baar baar write na hoti
        # ho field and not a primary key
    )
    component = models.ForeignKey(
        Component,
        on_delete=models.PROTECT,
        related_name="comp_issue_logs"
    )

    std_issue_quantity_issued = models.PositiveIntegerField()

    std_issue_form_date = models.DateField(null=True, blank=True)
    std_issue_issue_date = models.DateField(null=True, blank=True)
    std_issue_return_date = models.DateField(null=True, blank=True)

#ye foreign key refernece error dera but runtime pe sahi ho jayega
    def __str__(self):
        return f"{self.student.std_full_name}->{self.component.comp_name}"

