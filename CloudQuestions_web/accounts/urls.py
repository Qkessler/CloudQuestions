from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


# TODO: Set the urls.
# accounts/login/ [name='login']
# accounts/logout/ [name='logout']
# accounts/password_change/ [name='password_change']
# accounts/password_change/done/ [name='password_change_done']
# accounts/password_reset/ [name='password_reset']
# accounts/password_reset/done/ [name='password_reset_done']
# accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
# accounts/reset/done/ [name='password_reset_complete']

app_name = 'accounts'
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='login.html',
        redirect_field_name='questions/'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('reset/', auth_views.PasswordResetView.as_view(
        template_name='password_reset.html',
        email_template_name='password_reset.html'), name='password_reset'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.
         as_view(), name='password_reset_confirm'),
    path('reset/done', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
]
