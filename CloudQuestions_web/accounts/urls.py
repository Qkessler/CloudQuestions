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
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('reset/', auth_views.PasswordResetView.as_view(
        template_name='password_reset.html',
        email_template_name='password_reset.html'), name='password_reset'),
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done')
]
