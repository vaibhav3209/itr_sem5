from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone        #for current date
from django.db import transaction         # for no partial delete in student deletion
                                        # atomicity property


#keep in mind if the left  and right part are different they cause errors in dbms
# one is for admin view other is for database view
class Component(models.Model):
    CATEGORY_CHOICES = [
        ('Microcontrollers / Boards', 'Microcontrollers / Boards'),
        ('Sensors', 'Sensors'),
        ('Actuators', 'Actuators'),
        ('Electric Components', 'Electric Components'),
        ('Displays', 'Displays'),
        ('Miscellaneous', 'Miscellaneous'),
    ]

    COMPONENT_STATUS = [
        ('Defective', 'Defective'),
        ('Deleted', 'Deleted'),
        ("working", 'working')
    ]

    comp_category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    comp_name = models.CharField(max_length=100)
    comp_quantity_available = models.IntegerField()
    # comp_date_of_purchase = models.DateField()  # Optional: remove auto_now_add if you want to
    comp_status = models.CharField(max_length=10, choices=COMPONENT_STATUS, default="working")


    def __str__(self):
        return f"{self.comp_name} ({self.comp_category})"

class DeletedStudent(models.Model):
    del_std_roll_number = models.CharField(max_length=10,unique=True)
    del_std_first_name = models.CharField(max_length=30)
    del_std_last_name = models.CharField(max_length=30)
    del_std_college_email = models.EmailField(unique=True)
    del_std_deleted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" deleted logs for :{self.del_std_roll_number} on {self.del_std_deleted_at}"

class DeletedStudentIssueLog(models.Model):
    del_std_issue_roll_number = models.CharField(max_length=10)
    del_std_issue_component_name = models.CharField(max_length=100)
    del_std_issue_quantity_issued = models.PositiveIntegerField()
    del_std_issue_deleted_at = models.DateField(auto_now_add=True)
    del_std_issue_issue_date = models.DateField(null=True, blank=True)
    del_std_issue_return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return (f" deleted logs for :{self.del_std_issue_roll_number} on "
                f"{self.del_std_issue_deleted_at}")


class Student(models.Model):
    std_first_name = models.CharField(max_length=30)
    std_last_name = models.CharField(max_length=30)
    std_roll_number = models.CharField(max_length=10, unique=True)
    std_college_email = models.EmailField(unique=True)
    std_password = models.CharField(max_length=128)

    def set_password(self, raw_password):
        self.std_password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.std_password)

    def delete_with_history(self):
        with transaction.atomic():
            # Step 1: Copy to DeletedStudent
            DeletedStudent.objects.create(
                del_std_roll_number=self.std_roll_number,
                del_std_first_name=self.std_first_name,
                del_std_last_name=self.std_last_name,
                del_std_college_email=self.std_college_email,
                del_std_deleted_at=timezone.now()
            )
            # 2️ Copy ALL issue logs to DeletedStudentIssueLog
            for log in self.std_issue_logs.all():
                DeletedStudentIssueLog.objects.create(
                    del_std_issue_roll_number=self.std_roll_number,
                    del_std_issue_component_name=log.comp_name,
                    del_std_issue_quantity_issued=log.quantity_issued,
                    del_std_issue_deleted_at=timezone.now().date(),
                    del_std_issue_issue_date=log.issue_date,
                    del_std_issue_return_date=log.return_date
                )
            # 3️ Delete all issue logs
            self.std_issue_logs.all().delete()

            # 4 Delete student
            super().delete()

    @property
    def std_full_name(self):
        return f"{self.std_first_name} {self.std_last_name}"

    def __str__(self):
        return f"{self.std_full_name} ({self.std_roll_number})"





# delete all logs if student is deleted == >> cascade
#  prevent deletion if logs exist     == >> protect
class StudentIssueLog(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="std_issue_logs"
    )
    component = models.ForeignKey(
        Component,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="comp_issue_logs"
    )

    std_issue_quantity_issued = models.PositiveIntegerField()

    #isko mikemigration karna bach rha hai
    std_issue_form_date = models.DateField(null=True, blank=True)

    std_issue_issue_date = models.DateField(null=True, blank=True)
    std_issue_return_date = models.DateField(null=True, blank=True)

    STUDENT_STATUS_CHOICES = [
        ('Requested', 'Requested'),
        ('Issued', 'Issued'),
        ('Returned', 'Returned'),
        ('Rejectedbyteacher','Rejectedbyteacher')
    ]
    std_issue_status_from_student = models.CharField(
        max_length=20,
        choices=STUDENT_STATUS_CHOICES,
        blank=True,
        null=True
    )

    TEACHER_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Returned', 'Returned'),
    ]
    std_issue_status_from_teacher = models.CharField(
        max_length=20,
        choices=TEACHER_STATUS_CHOICES,
        default='Pending'
    )

#ye foreign key refernece error dera but runtime pe sahi ho jayega
    def __str__(self):
        return f"{self.student.std_full_name}->{self.component.comp_name}"



