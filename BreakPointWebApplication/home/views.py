from django.shortcuts import render

# Create your views here.

def welcome_page(request):
   return render(request, 'home/home.html')

def about_page(request):
   return render(request, 'home/about.html')