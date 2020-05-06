from django.shortcuts import render, redirect
from django.contrib.auth import login as log
from django.contrib.auth import authenticate
from django.http import HttpResponse
from .forms import SignUpForm


def index(request):
    return HttpResponse('Esta es la view base')


def register(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        email = form.cleaned_data.get('email')
        user = authenticate(username=username, password=password, email=email)
        log(request, user)
        return redirect('questions:index')
    return render(request, 'register.html', {'form': form})
