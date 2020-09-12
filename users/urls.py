# from django.urls import path
# from . import views
# from django.conf import settings
# from django.contrib.auth import views as auth_views
# from .views import CustomLoginView

# urlpatterns = [
#     path('', views.register, name='register'),
#     path('profile/', views.profile, name='profile'),
#     path('login/', CustomLoginView.as_view(template_name='users/login.html'), name='login'),
#     path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

# ]


# if settings.DEBUG:
#     from django.conf.urls.static import static
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)