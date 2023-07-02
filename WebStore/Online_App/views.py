from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from .models import AndroidApp, User_Profile, Screenshot
from .forms import AndroidAppForm, ScreenshotForm, CustomUserCreationForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from rest_framework import viewsets
from django.contrib import messages
import logging


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            if user.is_superuser:
                return redirect('admin_home')
            else:
                return redirect('user')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.user_profile.name = form.cleaned_data['name']
            user.user_profile.phone_number = form.cleaned_data['phone_number']
            user.user_profile.email = form.cleaned_data['email']
            user.user_profile.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def admin_home(request):
    if request.method == 'POST':
        form = AndroidAppForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.save()
            return redirect('admin_home')
    else:
        form = AndroidAppForm()
    apps = AndroidApp.objects.all()
    return render(request, 'admin_home.html', {'form': form, 'apps': apps})


@login_required
def user_home(request):
    user_profile = User_Profile.objects.get(user=request.user)
    screenshots = Screenshot.objects.filter(user_profile=user_profile)
    uploaded_apps = [screenshot.app for screenshot in screenshots]
    apps = AndroidApp.objects.all()
    app_details = []
    for app in apps:
        if app in uploaded_apps:
            app_details.append((app, True))  # Screenshot uploaded
        else:
            app_details.append((app, False))  # No screenshot uploaded

    return render(request, 'user_home.html', {'app_details': app_details, 'user_profile': user_profile})


@login_required
def upload_screenshot(request):
    user = request.user

    app_id = request.GET.get('app_id')  # Retrieve app_id from query parameters
    app = get_object_or_404(AndroidApp, id=app_id) if app_id else None

    user_profile = get_object_or_404(User_Profile, user=user)
    form = ScreenshotForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            screenshot = form.save(commit=False)
            screenshot.user_profile = user_profile
            screenshot.app = app
            screenshot.save()
            user_profile.points_earned += screenshot.app.points
            user_profile.tasks_completed += 1
            user_profile.save()
        return redirect('user')
    else:
        context = {
            'form': form,
            'app': app,
            'default_points': 0,
            'user_profile': user_profile,
        }
    return render(request, 'upload_screenshot.html', context)
@login_required
def profile_view(request):
    user_profile = User_Profile.objects.get(user=request.user)
    return render(request, 'profile_view.html', {'user_profile': user_profile})


@login_required
def points_view(request):
    # user = request.user
    user_profile = User_Profile.objects.get(user=request.user)
    points_earned = user_profile.points_earned
    screenshots = Screenshot.objects.filter(user_profile=user_profile)
    app_details = [(screenshot.app.name, screenshot.app.points) for screenshot in screenshots]
    context = {
        'points_earned': points_earned,
        'app_details': app_details
    }
    return render(request, 'points.html', context)


@login_required
def task_completed(request):
    user_profile = User_Profile.objects.get(user=request.user)
    tasks_completed = user_profile.tasks_completed
    screenshots = Screenshot.objects.filter(user_profile=user_profile)
    app_details = [(screenshot.app.name) for screenshot in screenshots]
    context = {
        'tasks_completed': tasks_completed,
        'app_details': app_details
    }
    return render(request, 'task_completed.html', context)
