from django.urls import path
from . import views

app_name = 'questions'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:topic>/', views.detail, name='detail'),
    path('upload_file/', views.upload_file, name='upload_file')
]
