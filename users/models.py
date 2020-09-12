from django.db import models
from django.contrib.auth import get_user_model
# from assignment.models import StudentOtherCourse



User = get_user_model()


COURSE_CHOICES = (
                ('', 'Select a course'),
                ('Integral Equations', 'Integral Equations'),
                ('Real Analysis', 'Real Analysis'),
)





# SELECT_COURSE = [(c.courses, c.courses) for c in SelectCourse.objects.all()]  



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='users/profile_pics/default1.png', upload_to='users/profile_pics')

    def __str__(self):
        return f'{self.user.index_number} profile'


