from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


# TODO: Set the urls.
# DONE accounts/login/ [name='login']
# DONE accounts/logout/ [name='logout']
# accounts/password_reset/ [name='password_reset']
# accounts/password_reset/done/ [name='password_reset_done']
# accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
# accounts/reset/done/ [name='password_reset_complete']

app_name = 'accounts'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html'),
         name='password_reset'),
]
