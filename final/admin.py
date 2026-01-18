from django.contrib import admin
from .models import Student, Component, StudentIssueLog,DeletedStudent,DeletedStudentIssueLog

admin.site.register(Student)
admin.site.register(Component)

#abhi isko nhi kiya
# @admin.register(Component)
# class ComponentAdmin(admin.ModelAdmin):
#     list_display = ('name', 'category', 'quantity', 'status', 'date_of_purchase')
#     list_filter = ('category',)
#     search_fields = ('name',)
#
#     def status(self, obj):
#         return obj.status
#
#
admin.site.register(StudentIssueLog)
admin.site.register(DeletedStudent)
admin.site.register(DeletedStudentIssueLog)
