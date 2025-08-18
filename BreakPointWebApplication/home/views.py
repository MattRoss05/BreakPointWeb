from django.shortcuts import render, redirect, get_object_or_404
from .models import Player, Match
from .forms import MatchForm
from django.contrib import messages
from django.db.models import Q
# Create your views here.

def welcome_page(request):
   player_list = Player.objects.all().order_by('-rank')
   context = {
      'player_list' : player_list
   }
   return render(request, 'home/home.html', context)

def display_rank(request):
   if request.user.is_authenticated:
      player_list = Player.objects.all().order_by('-rank')
      player = get_object_or_404(Player, user = request.user)
      context = {
      'player_list' : player_list,
      'win_count' : player.wins,
      'loss_count' : (player.matches-player.wins),
      'win_ratio' : round((player.wins/player.matches),2),

      
      }
      return render(request, 'home/rankings.html', context)
   else:
      player_list = Player.objects.all().order_by('-rank')
      context = {
         'player_list' : player_list,
      }
      return render(request, 'home/rankings.html', context)


def about_page(request):
   return render(request, 'home/about.html')


def match_page(request):
   if request.method == "POST":
      form = MatchForm(request.POST, user = request.user)
      if form.is_valid():
         form.save()
         return redirect('welcome')
   else:
      form = MatchForm(user = request.user)
   return render(request, 'home/match.html', {'form': form})

