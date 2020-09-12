def view_pdf(request, pk):
    # try:
    import os
    from django.conf import settings
    get_file = Profile.objects.get(pk=pk)
    f_name = os.path.join(settings.MEDIA_ROOT, str(get_file.attachment))
    file_name, file_ext = os.path.splitext(f_name)
    print(file_ext)
    if file_ext in ['.pdf', '.txt', '.py']:
        pdf = open(f_name, 'rb').read()
        return HttpResponse(pdf, content_type='application/'+file_ext[1:])
    elif file_ext in ['.jpeg', '.png', '.jpg', '.gif']:
        image = open(f_name, 'rb').read()
        return HttpResponse(image, content_type='image/'+file_ext[1:])
    elif file_ext in ['.mp4', '.mkv', '.MKV']:
        video = open(f_name, 'rb').read()
        return HttpResponse(video, content_type='video/'+file_ext[1:])
    elif file_ext in ['.mp4', '.mp3']:
        audio = open(f_name, 'rb').read()
        return HttpResponse(audio, content_type='audio/'+file_ext[1:])

    
    




    # response = FileResponse(open(f_name, 'rb'), content_type='application/pdf')
    # response['Content-Disposition'] = 'filename=some_file.pdf'
    # return response
    


u = User.objects.get(index_number=user)
    a = Assignment.objects.get(index=user)
    form = StudentResultForm2(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            title = form.cleaned_data.get('title')
            status = form.cleaned_data.get('status')
            scored = form.cleaned_data.get('scored')
            total = form.cleaned_data.get('total')
            marker = form.cleaned_data.get('marker')
            date_graded = form.cleaned_data.get('date_graded')
            obj = StudentResult.objects.create(title=title, status=status, scored=scored, 
                            total=total, marker=marker, date_graded=date_graded, user=u, assignment=a)
            return HttpResponseRedirect(reverse('submit-assignment'))
    else:
        form = StudentResultForm2()



        # ----------------------
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),


        # -------------------------------------
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hplgejos',
        'USER':'hplgejos',
        'PASSWORD':'R7LJtG0M-oZbohXE9lWAavrT8s5XBb6A',
        'HOST':'lallah.db.elephantsql.com',
        'PORT':'5432',


        # ----------------------------------------------------------------------------------------

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.http import JsonResponse
from .forms import (ImageFileUploadForm, FilesForm, StudentResultForm, 
                        StudentResultForm2, UploadedFileForm, 
                        RegisterCourseForm, SemesterForm, SelectCourseForm, StudentOtherCourseForm)
from .models import (Profile, Assignment, StudentResult, 
        UploadedFile, RegisterCourse, Semester, StudentOtherCourse, SelectCourse)
from django.contrib.auth import get_user_model
from django.views.generic import UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist
import datetime
import os
import random
from django.conf import settings
from django.http import FileResponse, Http404, HttpResponse, HttpResponseRedirect
from django.utils import timezone
from datetime import datetime as dt
from encrypted_id import ekey
# from users.models import SelectCourse

User = get_user_model()

@login_required
def submit_assignment(request, pk):
    o_t = StudentOtherCourse.objects.get(pk=pk)
    # user = User.objects.get(pk=o_t.user.pk)
    # sel = SelectCourse.objects.get(courses=user.course)
    # us = User.objects.filter(course=o_t.choose_course).exclude(index_number=request.user) #filter(course=s_c.courses)
    s = Semester.objects.first()
    rn = random.randint(1, 200)
    date = datetime.date.today()
    if request.method == 'POST':
        form = FilesForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            submission_date = ""
            try:
                u = UploadedFile.objects.filter(course=o_t.choose_course).first()
                submission_date = str(u.submission_date) # will come from database
            except AttributeError:
                return HttpResponseRedirect(reverse('assignment_app:submission-denied', args=(o_t.id,)))
            curr_date = str(date)
            # if curr_date <= submission_date:
            pdf_file = form.cleaned_data.get('file')
            _, e = os.path.splitext(str(pdf_file))
            if e in ['.pdf', 'txt']:
                assignment = Assignment.objects.create(pdf_file=pdf_file,
                            index=o_t.user.index_number, status='submitted', q_number=rn, date_submitted=date, date_created=timezone.now(), user=o_t.user, course=o_t.choose_course)
                return HttpResponseRedirect(reverse('assignment_app:submit-assignment', args=(o_t.pk,)))
            else:
                return JsonResponse({'error': True, 'errors': 'File type('+e+') not supported'})
            # else:
            #     return HttpResponseRedirect(reverse('assignment_app:submission-denied', args=(user.pk,)))

    else:
        form = FilesForm()

    # print(UploadedFile.objects.filter(course=o_t.choose_course))
    context = {
        'assignment': Assignment.objects.filter(user=o_t.user).filter(course=o_t.choose_course).order_by('-date_created'),
        'assigncount': Assignment.objects.filter(user=o_t.user).count(),
        'u_file': UploadedFile.objects.filter(course=o_t.choose_course),
        'c_file': UploadedFile.objects.all(),
        'result': StudentResult.objects.order_by('-date_graded1').filter(user=o_t.user),
        'prof': o_t.user,
        's': s,
        # 'sel': sel,
        # 'us': us,
        'o_t': o_t,
     
    }
    
    return render(request, 'assignment/index.html', context)


def query_results(request, pk):
    a = Assignment.objects.get(pk=pk)
    r = StudentResult.objects.filter(q_number=a.q_number)
    print(r)
    return HttpResponseRedirect(reverse('assignment_app:submit-assignment', args=(a.pk,)))



def submission_denied(request, pk):
    context = {
        'cur_user': User.objects.get(pk=pk)
    }
    return render(request, 'assignment/submission_denied.html', context)


def dashboard(request):

    if request.user.is_staff or request.user.is_superuser:
        return HttpResponseRedirect(reverse('assignment_app:all-courses', args=(request.user.pk,)))
    return HttpResponseRedirect(reverse('assignment_app:student-dashboard'))

    user = User.objects.get(index_number=request.user.index_number)
    context = {
        'u': user
    }
    return render(request, 'assignment/dashboard.html', context)



@login_required
def del_assignment(request, pk):
    import os
    
    ass = Assignment.objects.get(pk=pk)
    o_t = StudentOtherCourse.objects.get(choose_course=ass.course)
    us = ass.user.id
    date = datetime.date.today()
    submission_date = ''
    try:
        u = UploadedFile.objects.first()
        submission_date = str(u.submission_date)
    except AttributeError:
        return HttpResponseRedirect(reverse('assignment_app:submission-denied', args=(o_t.pk,)))
    curr_date = str(date)
    if curr_date <= submission_date:
        f_name = os.path.join(settings.MEDIA_ROOT, str(ass.pdf_file))
        ass.delete()
        os.remove(f_name)
        return HttpResponseRedirect(reverse('assignment_app:submit-assignment', args=(o_t.pk,)))
    return HttpResponseRedirect(reverse('assignment_app:submission-denied', args=(o_t.pk,)))


@login_required
def update_assignment(request, pk):
    ass = get_object_or_404(Assignment, pk=pk)
    form = FilesForm(request.POST or None,
                    request.FILES or None)
    return HttpResponseRedirect(reverse('assignment_app:submit-assignment'))


@login_required
def viewAssignmentPDF(request, pk):
    import os
    from django.conf import settings
    get_file = Assignment.objects.get(pk=pk)
    f_name = os.path.join(settings.MEDIA_ROOT, str(get_file.pdf_file))
    file_name, file_ext = os.path.splitext(f_name)
    if file_ext in ['.pdf', '.txt', '.py']:
        pdf = open(f_name, 'rb').read()
        return HttpResponse(pdf, content_type='application/'+file_ext[1:])


def django_image_and_file_upload_ajax(request):
    if request.method == 'POST':
       form = ImageFileUploadForm(request.POST, request.FILES)
       if form.is_valid():
           form.save()
           
           return JsonResponse({'error': False, 'message': 'Uploaded Successfully'})
       else:
           return JsonResponse({'error': True, 'errors': form.errors})
    else:
        form = ImageFileUploadForm()
        return render(request, 'assignment/upload.html', {'form': form})



def show_files(request):
    obj = Profile.objects.all()
    return render(request, 'assignment/show_files.html', {'object': obj})


@login_required
@staff_member_required
def student_result(request, pk):
    # user = User.objects.get(pk=pk)
    o_c1 = StudentOtherCourse.objects.get(pk=pk)
    o_c = StudentOtherCourse.objects.filter(choose_course=o_c1.choose_course)
    # sel = SelectCourse.objects.filter(courses=user.course).first()
    
    try:
        # u = User.objects.get(pk=pk)
        a = Assignment.objects.filter(index=o_c1.user.index_number).first()
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('assignment_app:score-student-section', args=(pk,)))
    if request.method == 'POST':
        form = StudentResultForm(request.POST)
        if form.is_valid:
            obj = form.save(commit=False)
            form.instance.user = o_c1.user
            form.instance.assignment = a
            # update status in assignment
            obj.status = form.cleaned_data.get('status')
            # a1 = Assignment.objects.get(index=u.index_number)
            a = Assignment.objects.filter(index=a).update(status=obj.status)
            form.save()

            return HttpResponseRedirect(reverse('assignment_app:score-student-section', args=(pk,)))
    else:
        form = StudentResultForm()
    
    s_a = Assignment.objects.order_by('-date_created').filter(index=o_c1.user.index_number)
    context = {
        'form': form,
        'ass': s_a,
        'u': o_c1.user,
        'sel': o_c,
        'o_c1': o_c1,
    }
    return render(request, 'assignment/studentresult_update_form.html', context)


@login_required
@staff_member_required
def all_students(request, pk):
    o_c1 = StudentOtherCourse.objects.get(pk=pk)
    print(o_c1.choose_course)
    all_staff = User.objects.filter(is_staff=True)
    user = User.objects.exclude(index_number__in=all_staff)
    # s_c = SelectCourse.objects.get(pk=pk)
    # u = User.objects.get(pk=s_c.user.pk)
    
    o_c = StudentOtherCourse.objects.filter(choose_course=o_c1.choose_course)
    ie_users = User.objects.filter(course=o_c1.choose_course).exclude(index_number__in=all_staff) #filter(course=s_c.courses)
    query = request.GET.get('q')
    if query:
        ie_users = User.objects.filter(index_number=query)
        ra_users = User.objects.filter(index_number=query)
    if request.method == 'POST':
        form = UploadedFileForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            file = form.cleaned_data.get('pdf_file')
            date_to_subm = form.cleaned_data.get('submission_date')
            date = datetime.date.today()
            # if UploadedFile.objects.count() > 0:
            #     u = UploadedFile.objects.first()
            #     u.pdf_file = file
            #     u.date_created = date
            #     u.submission_date = date_to_subm
            #     u.save()
            #     return HttpResponseRedirect(reverse('assignment_app:all-students', args=(pk,)))
            # else:
            f = UploadedFile.objects.create(pdf_file=file, date_created=date, course=o_c1.choose_course, submission_date=date_to_subm, user=request.user, selectcourse=o_c1)

            return HttpResponseRedirect(reverse('assignment_app:all-students', args=(pk,)))
    else:
        form = UploadedFileForm()


    context = {
        'form': form,
        'all_students': user,
        # 'ra_users': ra_users,
        'ie_users': ie_users,
        'semester': Semester.objects.first(),
        'o_c1': o_c1,
        'o_c': o_c,
        'u_file': UploadedFile.objects.filter(course=o_c1.choose_course),
    }
    return render(request, 'assignment/all_students.html', context)



def del_upload_file(request, pk):
    u = UploadedFile.objects.get(pk=pk)
    u.delete()
    return HttpResponseRedirect(reverse('assignment_app:all-students', args=(u.selectcourse.pk,)))



def download_pdf(request, pk):
    import os
    from django.conf import settings
    get_file = UploadedFile.objects.filter(pk=pk).first()
    f_name = os.path.join(settings.MEDIA_ROOT, str(get_file.pdf_file))
    file_name, file_ext = os.path.splitext(f_name)
    if file_ext in ['.pdf', '.txt', '.py']:
        pdf = open(f_name, 'rb').read()
        return HttpResponse(pdf, content_type='application/'+file_ext[1:])


class GradeUpdateView(UpdateView):
    model = StudentResult
    fields = ['title', 'status', 'scored', 'total', 'marker', 'date_graded']

    template_name_suffix = '_update_form'
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False


def main_dashboard(request, pk):
    cur_user = User.objects.get(pk=pk)
    context = {
        'cur_user': cur_user,
    }
    return render(request, 'assignment/main_dashboard.html', context)


def register_course(request, pk):
    user = User.objects.get(pk=pk)
    if request.method == 'POST':
        form = RegisterCourseForm(request.POST)
        if form.is_valid():
            form.instance.user = user
            form.save()
            return HttpResponseRedirect(reverse('assignment_app:all-students'))
    else:
        form = RegisterCourseForm(instance=user)
    context = {
        'form': form,
    }
    return render(request, 'assignment/assignment_update_form.html', context)


@staff_member_required
def update_submitted(request, pk):
    a1 = Assignment.objects.get(pk=pk)
    a = Assignment.objects.filter(index=a1).update(status='graded')
    return HttpResponseRedirect(reverse('assignment_app:score-student-section', args=(pk,)))


class StatusUpdateView(UpdateView):
    model = Assignment
    fields = ['status']

    template_name_suffix = '_update_form'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False

def all_courses(request, pk):
    s = SelectCourse.objects.all()
    o_c = StudentOtherCourse.objects.all()
    # --------------------
    for o in o_c:
        print(o.selectcourse.pk)
    # ------------------
    
    


    # create course
    if request.method == 'POST':
        c_form = SelectCourseForm(request.POST)
        if c_form.is_valid():
            c_form.instance.user = request.user
            c_form.save()
            return HttpResponseRedirect(reverse('assignment_app:all-courses', args=(pk,)))
    else:
        c_form = SelectCourseForm()

    #  set semester
    if request.method == 'POST':
        s_form = SemesterForm(request.POST)
        if s_form.is_valid():
            obj = s_form.save(commit=False)
            obj.sem = s_form.cleaned_data.get('sem')
            if Semester.objects.count() == 0:
                s_form.save()
            else:
                s = Semester.objects.first()
                s.sem = obj.sem
                s.save()
            return HttpResponseRedirect(reverse('assignment_app:all-courses', args=(pk,)))
    else:
        s_form = SemesterForm()

    context = {
        # 'a_c': s,
        'o_c': o_c,
        # 'o_c1': o_c1,
        's_form': s_form,
        'c_form': c_form,
        'semester': Semester.objects.first(),    }
    return render(request, 'assignment/all_courses.html', context)



def del_course(request, pk):
    # print(pk)
    # u = User.objects.get(pk=request.user.pk)
    s = StudentOtherCourse.objects.filter(pk=pk)
    # s = SelectCourse.objects.get(pk=pk)
    s.delete()
    return HttpResponseRedirect(reverse('assignment_app:all-courses', args=(s.user.pk,)))

def student_dashboard(request):
    user = User.objects.get(pk=request.user.pk)
    if request.method == 'POST':
        o_form = StudentOtherCourseForm(request.POST)
        if o_form.is_valid():
            fm = o_form.save(commit=False)
            fm.choose_course = o_form.cleaned_data.get('choose_course')
            s = SelectCourse.objects.get(courses=fm.choose_course)
            o_form.instance.selectcourse = s
            o_form.instance.user = request.user
            o_form.save()
            return HttpResponseRedirect(reverse('assignment_app:student-dashboard'))
    else:
        o_form = StudentOtherCourseForm()

    o_course = StudentOtherCourse.objects.filter(user=request.user)
    context = {
        'o_form': o_form,
        'o_course': o_course,
    }
    return render(request, 'assignment/student_dashboard.html', context)

def to_submit_assignment(request, pk):
    return HttpResponseRedirect(reverse('assignment_app:submit-assignment', args=(pk,)))
