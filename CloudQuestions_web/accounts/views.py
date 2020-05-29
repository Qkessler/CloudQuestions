from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import authenticate
from .forms import SignUpForm, SwitchForm
from social_django.models import UserSocialAuth
from accounts.src.api_client import get_url, get_flow, calendar_connection
from accounts.src.api_client import create_event
from questions.src import question_service
from oauth2client.contrib import xsrfutil
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
import httplib2
import os

CALENDAR_API_KEY = os.environ['CALENDAR_API_KEY']
SCOPE_EVENTS = 'https://www.googleapis.com/auth/calendar.events'
CALENDAR_REDIRECT_URI = 'http://127.0.0.1:8000/accounts/settings/'
EVENT_TOPIC = None
EVENT_COLOR = None


def register(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        email = form.cleaned_data.get('email')
        user = authenticate(username=username, password=password, email=email)
        login(request, user)
        question_service.create_calendar_connection(user)
        return redirect('questions:questions')
    return render(request, 'register.html', {'form': form})


@login_required
def settings(request, topic=None, color=None):
    global EVENT_TOPIC
    global EVENT_COLOR
    context = {}
    user = request.user
    table = question_service.create_table(user)
    user_calendar = question_service.get_calendar(request.user)
    context['ratings_table'] = table
    flow = get_flow()
    if topic and color and user_calendar:
        EVENT_TOPIC = topic
        EVENT_COLOR = color
        return redirect(get_url(flow), topic, color)
    if request.GET.get('code'):
        code = request.GET.get('code')
        service = calendar_connection(code, flow)
        create_event(EVENT_TOPIC, EVENT_COLOR, service)
    if request.GET.get('calendar'):
        question_service.change_calendar_connection(user)
        return redirect('accounts:settings')
    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None

    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
        twitter_login = None

    try:
        google_login = user.social_auth.get(provider='google-oauth2')
    except UserSocialAuth.DoesNotExist:
        google_login = None

    can_disconnect = (user.social_auth.count() > 1 or
                      user.has_usable_password())
    context['calendar_connection'] = user_calendar
    context['github_login'] = github_login
    context['twitter_login'] = twitter_login
    context['google_login'] = google_login
    context['can_disconnect'] = can_disconnect
    return render(request, 'settings.html', context)
