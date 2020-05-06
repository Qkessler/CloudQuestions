from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='login.html',
        redirect_field_name='questions/'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='login.html',
        redirect_field_name='questions:index'), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='password_reset.html',
        email_template_name='password_reset.html'), name='password_reset'),
    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done')
]
