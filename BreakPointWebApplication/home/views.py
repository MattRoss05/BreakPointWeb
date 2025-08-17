from django.shortcuts import render
from .models import Player
# Create your views here.

def welcome_page(request):
   player_list = Player.objects.all().order_by('-rank')
   context = {
      'player_list' : player_list
   }
   return render(request, 'home/home.html', context)
def display_rank(request):
   player_list = Player.objects.all().order_by('-rank')
   context = {
      'player_list' : player_list
   }
   return render(request, 'home/rankings.html', context)

def about_page(request):
   return render(request, 'home/about.html')