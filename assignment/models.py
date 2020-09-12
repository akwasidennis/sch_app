from django.db import models
from .utils import Utils
from django.urls import reverse
from django.db import OperationalError
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
# from users.models import SelectCourse

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    photo = models.ImageField(upload_to="images/")
    attachment = models.FileField(upload_to="attachments/")
    phone = models.CharField(max_length=10)



class RegisterCourse(models.Model):
    CLASS_CHOICES = (
                ('', 'Select class'),
                ('Math1', 'Math 1'),
                ('Math2', 'Math 2'),
                ('Math3', 'Math 3'),
                ('Math4', 'Math 4'),
                )

    COURSE_CHOICES = (
                ('', 'Select a course'),
                ('Integral Equations', 'Integral Equations'),
                ('Real Functions', 'Real Functions'),
                )

    course = models.CharField(choices=COURSE_CHOICES, max_length=100)
    class_or_level = models.CharField(choices=CLASS_CHOICES, max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('assignment_app:submit-assignment', kwargs={'pk': self.user.pk})
    

    def __str__(self):
        return f'{self.user.index_number} {self.course} ({self.class_or_level})'


COLOR_CHOICES = (
                ('', 'Select back color'),
                ('green', 'green'),
                ('blue', 'blue'),
                ('red', 'red'),
                ('burlywood', 'burlywood'),
                ('darkkhaki', 'darkkhaki'),
                ('darkslateblue', 'darkslateblue'),
                ('deeppink', 'deeppink'),
                ('fuchsia', 'fuchsia'),
                ('gold', 'gold'),
                ('indigo', 'indigo'),

                )

class SelectCourse(models.Model):
    courses = models.CharField(_('Course name'), max_length=200)
    choose_back_color = models.CharField(_('Course background'), default='black', max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.courses} -----> {self.choose_back_color}'


class StudentOtherCourse(models.Model):
    choose_course = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    selectcourse = models.ForeignKey(SelectCourse, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.choose_course




STATUS = (
        ('graded', 'graded'),
        ('ungraded', 'ungraded'),
    )



class Assignment(models.Model):
    pdf_file = models.FileField(upload_to="activity/")
    index = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    q_number = models.IntegerField()
    date_submitted = models.DateField(default=Utils.get_date)
    date_created = models.DateTimeField(default=Utils.get_date_time)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    studentothercourse = models.ForeignKey(StudentOtherCourse, on_delete=models.CASCADE)
    course = models.CharField(max_length=200)

    def get_absolute_url(self):
        return reverse('assignment_app:submit-assignment', kwargs={'pk': self.pk})
    

    def __str__(self):
        return f'{self.index}'

    def encoded_id(self):
        import base64
        return base64.b64encode(str(self.user_id))

    def decode_id(self, id):
        import base64
        return base64.b64decode(id)


class StudentResult(models.Model):
    TITLE = (
            ('', 'select title'),
            ('assignment', 'Assignment'),
             ('exercise', 'Exercise'),
             ('quiz', 'Quiz'),
    )

    STATUS = (
            ('', 'select status'),
            ('graded', 'graded'),
             ('not graded', 'not graded'),
    )
    q_number = models.IntegerField()
    title = models.CharField(max_length=50, choices=TITLE)
    status = models.CharField(max_length=50, choices=STATUS)
    scored = models.FloatField()
    total = models.FloatField()
    course = models.CharField(max_length=200)
    marker = models.CharField(max_length=200)
    date_graded = models.DateField(default=Utils.get_date)
    date_graded1 = models.DateTimeField(default=Utils.get_date_time)    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    studentothercourse = models.ForeignKey(StudentOtherCourse, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}'

    @property
    def get_percentage(self):
        p = (self.scored / self.total) * 100
        return p

    def get_absolute_url(self):
        return reverse('assignment_app:all-students', kwargs={'pk': self.studentothercourse.selectcourse.id})



class Semester(models.Model):
    SEMESTER = (
        ('', 'select semester'),
        ('semester one', 'SEMESTER ONE'),
        ('semester two', 'SEMESTER TWO'),
    )
    sem = models.CharField(max_length=100, choices=SEMESTER)



       
# SELECT_COURSE = [(c.courses, c.courses) for c in SelectCourse.objects.all()]  

SELECT_COURSE = [('Integral Equations', 'Integral Equations'),
                ('Real Ananlysis', 'Real Analysis'),
                ('Optimization', 'Optimization')]

class UploadedFile(models.Model):
    pdf_file = models.FileField(upload_to="activity/")
    date_created = models.DateTimeField(default=Utils.get_date_time)
    course = models.CharField(max_length=200)
    submission_date = models.DateField(default=Utils.get_date_time)
    attach_info = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    selectcourse = models.ForeignKey(SelectCourse, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'



