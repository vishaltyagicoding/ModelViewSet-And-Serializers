from django.contrib import admin

# Register your models here.
from .models import College, Course, Branch, Student
@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    list_filter = ('name', 'location')
    search_fields = ('name', 'location')

    fieldsets = (
        ('College Information', {
            'fields': ('name', 'location')
        }),
    )
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    list_filter = ('name', 'code')
    search_fields = ('name', 'code')

    fieldsets = (
        ('Course Information', {
            'fields': ('name',)
        }),
    )
@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    list_filter = ('name', 'code')
    search_fields = ('name', 'code')

    fieldsets = (
        ('Branch Information', {
            'fields': ('name', 'code')
        }),
    )
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'student_id')
    list_filter = ('name', 'email')
    search_fields = ('name', 'email', 'student_id')

    fieldsets = (
        ('Student Information', {
            'fields': ('name', 'email', 'student_id', 'course', 'college', 'branch')
        }),
    )