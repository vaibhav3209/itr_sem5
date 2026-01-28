from django.contrib import admin
from .models import Student, Component, StudentIssueLog, ComponentCategory, Branches

admin.register(ComponentCategory)
admin.register(Branches)


#for line 24,25
#if anything is foreign key aur usko yha likhte to vo print hota
#*****NOTE::*****    JO __STR()__ MEIN LIKHA HOGA
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("std_roll_number", "std_first_name", "std_last_name")
    search_fields = ("std_roll_number", "std_first_name", "std_last_name")
    list_filter = ("std_year_of_passing",)


@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ("comp_name", "comp_category", "comp_quantity_available")
    search_fields = ("comp_name",)
    list_filter = ("comp_category",)


@admin.register(StudentIssueLog)
class IssueLogAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "component",
        "std_issue_quantity_issued",
        "std_issue_issue_date",
        "std_issue_return_date",
    )
    list_filter = ("std_issue_issue_date", "std_issue_return_date")
    search_fields = ("student__std_roll_number", "component__comp_name")