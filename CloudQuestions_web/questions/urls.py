from django.urls import path
from . import views

app_name = 'questions'
urlpatterns = [
    path('', views.index, name='index'),
    path('create_topic', views.create_topic, name='create_topic'),
    path('<str:topic>/', views.detail, name='detail'),
    path('<str:topic>/random/', views.random_questions, name='random'),
    path('<str:topic>/random/<str:list_questions>',
         views.random_questions, name='random')
]
