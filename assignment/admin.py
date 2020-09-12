from django.contrib import admin
from .models import (Profile, Assignment, StudentResult, 
        UploadedFile, RegisterCourse, Semester, StudentOtherCourse, SelectCourse)


admin.site.site_header = "Students Record"
@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'studentothercourse', 'course', 'pdf_file', 'index', 'status', 'q_number', 'date_submitted']

@admin.register(StudentOtherCourse)
class StudentOtherCourseAdmin(admin.ModelAdmin):
    list_display = ['user', 'choose_course']

@admin.register(StudentResult)
class StudentResultAdmin(admin.ModelAdmin):
    list_display = ['q_number', 'title', 'status', 'scored', 'total', 'marker', 'date_graded', 'user', 'assignment']

@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ['user', 'selectcourse', 'course', 'pdf_file', 'date_created', 'submission_date']

@admin.register(RegisterCourse)
class RegisterCourseAdmin(admin.ModelAdmin):
    list_display = ['user', 'course']

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ['sem',]

@admin.register(SelectCourse)
class SelectCourseAdmin(admin.ModelAdmin):
    list_display = ['user', 'courses', 'choose_back_color', 'date_created']






