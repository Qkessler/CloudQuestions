from django.contrib import admin
from django.urls import path, include
from questions.views import index
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('', index, name='index'),
    path('questions/', include('questions.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('oauth/', include('social_django.urls', namespace='social')),
]

urlpatterns += staticfiles_urlpatterns()
