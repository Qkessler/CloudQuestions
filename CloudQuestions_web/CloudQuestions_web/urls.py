from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('questions/', include('questions.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('oauth/', include('social_django.urls', namespace='social')),
]
