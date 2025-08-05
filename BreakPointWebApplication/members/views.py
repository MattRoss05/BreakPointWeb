from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from . forms import CustomUserCreationForm


def logout_user(request):
    logout(request)
    messages.success(request,("You have logged out"))
    return redirect('welcome')

def register_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username, password = password)
            login(request, user)
            messages.success(request, ("You have joined!"))
            return redirect('welcome')
    else:
        form = CustomUserCreationForm()
    return render(request, 'members/register_user.html', {'form': form})