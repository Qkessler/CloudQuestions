from django.urls import path, include
from . import views


app_name = 'accounts'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('social-auth/', include('social_django.urls', namespace='social'))
]
