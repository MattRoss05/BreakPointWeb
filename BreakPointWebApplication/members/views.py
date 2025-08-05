from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm


def logout_user(request):
    logout(request)
    messages.success(request,("You have logged out"))
    return redirect('welcome')