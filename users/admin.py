from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import UserRegisterForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile

User = get_user_model()




admin.site.register(UserProfile)


