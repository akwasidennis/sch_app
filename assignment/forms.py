from django import forms
from .models import (Profile, StudentResult, UploadedFile, 
                            Assignment, STATUS, Semester, StudentOtherCourse, SelectCourse, COLOR_CHOICES)
from .utils import Utils
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from cruds_adminlte import ColorPickerWidget
from django.utils.translation import gettext_lazy as _

User = get_user_model()

# from users.models import SelectCourse

def get_my_choices():
    SELECT_COURSE = [(c.courses, c.courses) for c in SelectCourse.objects.all()]  
    return SELECT_COURSE


class DateInput(forms.DateInput):
    input_type = 'date'
# --------------------------------------------------------------
class ImageFileUploadForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'photo', 'attachment',) 


class StudentResultForm(forms.ModelForm):
    q_number = forms.CharField(help_text='Enter the q number above', max_length=50)
    date_graded = forms.DateField(widget=DateInput)
    course = forms.CharField(max_length=200)
    def __init__(self, o_c1, user, *args, **kwargs):
        self.user = user
        self.o_c1 = o_c1
        print()
        super(StudentResultForm, self).__init__(*args, **kwargs)
        self.fields['course'] = forms.CharField(initial=self.o_c1.choose_course, disabled=True)  #widget=forms.Select(choices=get_my_choices())

    class Meta:
        model = StudentResult
        fields = ('q_number', 'course', 'title', 'status', 'scored', 'total', 'marker', 'date_graded',)
 

    # def clean_course(self):
    #     course = self.cleaned_data.get('course')
    #     q_number = self.cleaned_data.get('q_number')
    #     a = Assignment.objects.filter(user=self.o_c1.user).filter(course=course).filter(q_number=q_number)
    #     print(a)
        # if r.count() > 0:
        #     # raise ValidationError(f'Student with this query number, {q_number} has already been graded!')
        #     return JsonResponse({'error': True, 'errors': 'File type not supported'})
        # return q_number



class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ('sem',)
 

class StudentResultForm2(forms.Form):
    TITLE = (
            ('assignment', 'Assignment'),
             ('exercise', 'Exercise'),
             ('quiz', 'Quiz'),
    )

    STATUS = (
            ('graded', 'graded'),
             ('not graded', 'graded'),
    )
    title = forms.ChoiceField(choices=TITLE, help_text='title')
    status = forms.ChoiceField(choices=STATUS, help_text='status')
    scored = forms.FloatField()
    total = forms.FloatField()
    marker = forms.CharField(max_length=200)
    date_graded = forms.DateField()
    

class FilesForm(forms.Form):
    file = forms.FileField()



class UploadedFileForm(forms.Form):
    pdf_file = forms.FileField()
    attach_info = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Add any descriptions to the file. \nNB: It\'s optional', 'rows':5,}), required=False)
    submission_date = forms.DateField(widget=DateInput)  # forms.TextInput(attrs={'placeholder':'2020-08-22'}


class RegisterCourseForm(forms.ModelForm): 
    status = forms.CharField(widget=forms.Select(choices=STATUS), max_length=50)
    class Meta:
        model = Assignment
        fields = ('status',)



class SelectCourseForm(forms.ModelForm):
    class Meta:
        model = SelectCourse
        fields = ('courses', 'choose_back_color',)

    choose_back_color = forms.CharField(widget=forms.Select(choices=COLOR_CHOICES), max_length=50, required=False)

    def clean_courses(self):
        courses = self.cleaned_data.get('courses')
        user = self.cleaned_data.get('user')
        o = SelectCourse.objects.filter(courses=courses)
        if o.count() > 0:
            raise ValidationError(f'{courses} has already been created!')
        return courses


class StudentOtherCourseForm(forms.ModelForm):
    # choose_course = forms.CharField(max_length=50)
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(StudentOtherCourseForm, self).__init__(*args, **kwargs)
        self.fields['choose_course'] = forms.CharField(
            widget=forms.Select(choices=get_my_choices()) )

    class Meta:
        model = StudentOtherCourse
        fields = ('choose_course',)

    def clean_choose_course(self):
        choose_course = self.cleaned_data.get('choose_course')
        user = self.cleaned_data.get('user')
        o = StudentOtherCourse.objects.filter(user=self.user).filter(choose_course=choose_course)

        if o.count() > 0:
            raise ValidationError(f'{choose_course} has already been registered!')
        return choose_course

