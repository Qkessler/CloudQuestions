from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from django.http import HttpResponse
from .forms import SignUpForm


def index(request):
    return HttpResponse('Esta es la view base')


# TODO: Create a logout view that takes you to the questions:index view.
def logout_view(request):
    if request.user.is_authenticated:
        logout()
    return redirect('questions:index')


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
