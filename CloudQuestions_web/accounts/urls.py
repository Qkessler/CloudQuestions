from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('settings/', views.settings, name='settings'),
    path('settings/<str:topic>/<str:color>', views.settings, name='settings')
]
