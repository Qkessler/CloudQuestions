from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import authenticate
from .forms import SignUpForm, SwitchForm
from social_django.models import UserSocialAuth
from  questions.src import question_service


def register(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        email = form.cleaned_data.get('email')
        user = authenticate(username=username, password=password, email=email)
        login(request, user)
        return redirect('questions:index')
    return render(request, 'register.html', {'form': form})


@login_required
def settings(request):
    context = {}
    user = request.user
    table = question_service.create_table(user)
    context['ratings_table'] = table

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

    form = SwitchForm(request.POST)
    if form.is_valid():
        form.save()
        on = form.cleaned_data.get('')
        print(on)
    context['switch'] = form
    can_disconnect = (user.social_auth.count() > 1 or
                      user.has_usable_password())
    context['github_login'] = github_login
    context['twitter_login'] = twitter_login
    context['google_login'] = google_login
    context['can_disconnect'] = can_disconnect
    return render(request, 'settings.html', context)
