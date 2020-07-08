import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import (urlsafe_base64_encode, urlsafe_base64_decode)
from .forms import (SignUpForm, ChangeUsernameForm,
                    ChangeEmailForm, RemoveAccountForm)
from social_django.models import UserSocialAuth
from accounts.src.api_client import get_url, get_flow, calendar_connection
from accounts.src.api_client import create_event
from questions.src import question_service
from django.contrib.auth.models import User


def register(request):
    form = SignUpForm(request.POST)
    context = {}
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        email = form.cleaned_data.get('email')
        user = authenticate(username=username, password=password,
                            email=email)
        user.is_active = False
        user.save()
        breakpoint()
        question_service.create_calendar_connection(user)
        current_site = get_current_site(request)
        mail_subject = 'Activate your CloudQuestions account!'
        message = render_to_string('verify_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        email_message = EmailMessage(
            mail_subject, message, to=[email]
        )
        email_message.send()
        return render(request, 'verify.html')
    context['form'] = form
    return render(request, 'register.html', context)


def activate(request, uidb64, token):
    context = {}
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        context['active'] = True
    return render(request, 'activated.html', context)


@login_required
def settings(request, topic=None, color=None):
    if request.GET.get('toggle_help'):
        return redirect('questions:detail', 'CloudQuestions_Help')
    context = {}
    user = request.user
    table = question_service.create_table(user)
    user_calendar = question_service.get_calendar(request.user)
    flow = get_flow(topic, color)
    if topic and color and user_calendar:
        return redirect(get_url(flow))
    if request.GET.get('code'):
        code = request.GET.get('code')
        topic, color = request.GET.get('state').split('+')
        service = calendar_connection(code, flow)
        create_event(topic, color, service)
    if request.GET.get('calendar'):
        question_service.change_calendar_connection(user)
        return redirect('accounts:settings')
    if request.GET.get('remove_account'):
        context['remove_pressed'] = True
    change_user_form = ChangeUsernameForm(user_name=user.username)
    change_email_form = ChangeEmailForm(user_email=user.email)
    remove_account_form = RemoveAccountForm()
    if request.method == 'POST':
        if request.POST.get('action') == 'email_form':
            change_email_form = ChangeEmailForm(request.POST)
            user.email = request.POST.get('email')
            user.save()
        elif request.POST.get('action') == 'user_form':
            change_user_form = ChangeUsernameForm(request.POST)
            user.username = request.POST.get('username')
            user.save()
        elif request.POST.get('action') == 'remove_account':
            remove_account_form = RemoveAccountForm(request.POST)
            if request.POST.get('username') == user.username:
                user.delete()
    context['change_user_form'] = change_user_form
    context['change_email_form'] = change_email_form
    context['remove_account_form'] = remove_account_form
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
    context['ratings_table'] = table
    context['user'] = user
    return render(request, 'settings.html', context)
