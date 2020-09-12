from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from .forms import (UserRegisterForm, 
                UserProfileUpdateForm, UserUpdateForm)
from assignment.models import StudentOtherCourse, Assignment, SelectCourse
User = get_user_model()

def register(request):
    if request.method == 'POST':
        u_form = UserRegisterForm(request.POST)
        if u_form.is_valid():
            u_form.save()
            index_number = u_form.cleaned_data.get('index_number')
            index_num = u_form.cleaned_data.get('index')
            messages.success(request, "Registered successfully!!!")
            return HttpResponseRedirect(reverse('login'))
    else:
        u_form = UserRegisterForm()
    context = {
        'u_form': u_form, 
    }
    return render(request, 'users/register.html', context)



@login_required
def profile(request, pk, i_n):
    sel = SelectCourse.objects.get(pk=pk)
    o_t = StudentOtherCourse.objects.get(id=i_n)

    # o_t = StudentOtherCourse.objects.filter(choose_course=sel.courses).first()
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=o_t.user)
        p_form = UserProfileUpdateForm(request.POST, request.FILES, instance=o_t.user.userprofile)
        if u_form.is_valid and p_form.is_valid:
            u_form.save()
            p_form.save()
            messages.success(request, "Profile changed successfully!!!")
            return HttpResponseRedirect(reverse('profile', args=(sel.user.pk,i_n,)))
    else:
        u_form = UserUpdateForm(instance=o_t.user)
        p_form = UserProfileUpdateForm(instance=o_t.user.userprofile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'o_t': o_t,    
        'sel': sel,   
    }
    return render(request, 'users/profile.html', context)


def back(request, pk):
    u = User.objects.get(pk=pk)
    return HttpResponseRedirect(reverse('submit-assignment', args=(u.pk,)))

# class CustomLoginView(LoginView):
#     authentication_form = CustomAuthenticationForm


def login_success(request):
    if request.user.is_staff or request.user.is_superuser:
        messages.success(request, "Login successful!!!")
        return HttpResponseRedirect(reverse('assignment-section:all-courses'))
    else:
        messages.success(request, "Login successful!!!")
        return HttpResponseRedirect(reverse('assignment-section:submit-assignment'))


