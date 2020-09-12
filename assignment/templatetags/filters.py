from django import template
from assignment.models import Assignment, SelectCourse, StudentOtherCourse, StudentResult
from django.contrib.auth import get_user_model
import urllib
register = template.Library()

User = get_user_model()

@register.simple_tag
def count_assignment_of_student(pk):
    u = User.objects.get(pk=pk)
    a = Assignment.objects.filter(index=u).count()
    return a

@register.filter
def encode_id(pk):
    p = urllib.parse.urlencode(pk)
    return p
    

@register.simple_tag
def cal_course(pk):
    s = SelectCourse.objects.get(pk=pk)
    # o_c = StudentOtherCourse.objects.get(pk=pk)
    # u = User.objects.exclude(pk=s.pk).filter(course=s.courses).count()
    all_staff = User.objects.filter(is_staff=True)
    print(all_staff)
    o = StudentOtherCourse.objects.exclude(user__in=all_staff).filter(choose_course=s.courses).count()
    return o


@register.simple_tag
def courses():
    o_c = StudentOtherCourse.objects.all()
    return o_c




@register.simple_tag
def std_index(course, user):
    ind = StudentResult.objects.filter(user=user).filter(course=course)
    for r in ind:
        i = r.user.index_number
    return i

@register.simple_tag
def std_ass(course):
    ass = StudentResult.objects.filter(course=course).filter(title='assignment')
    for r in ass:
        i = r.scored
    return i

@register.simple_tag
def std_exx(course):
    exx = StudentResult.objects.filter(course=course).filter(title='exercise')
    for r in exx:
        i = r.scored
    return i

@register.simple_tag
def std_qzz(course):
    qzz = StudentResult.objects.filter(course=course).filter(title='quiz')
    for r in qzz:
        i = r.scored
    return i
