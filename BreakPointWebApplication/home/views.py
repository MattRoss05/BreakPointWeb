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
      player_list = Player.objects.filter(matches__gte = 5).order_by('-rank')
      player = get_object_or_404(Player, user = request.user)
      if player.matches == 0:
         win_ratio = 0
      else:
         win_ratio = round((player.wins/player.matches),2)
      context = {
      'player_list' : player_list,
      'player_rating' : player.rank,
      'win_count' : player.wins,
      'loss_count' : (player.matches-player.wins),
      'win_ratio' : win_ratio,

      
      }
      return render(request, 'home/rankings.html', context)
   else:
      player_list = Player.objects.filter(matches__gte = 5).order_by('-rank')
      context = {
         'player_list' : player_list,
      }
      return render(request, 'home/rankings.html', context)


def about_page(request):
   return render(request, 'home/about.html')


def match_page(request):
   if request.user.is_authenticated:

      if request.method == "POST":
         form = MatchForm(request.POST, user = request.user)
         if form.is_valid():
            form.save()
            request.session['can_access_display'] = True
            return redirect('message')
      else:
         form = MatchForm(user = request.user)
      return render(request, 'home/match.html', {'form': form})
   else:
      request.session['can_access_forbidden'] = True
      return redirect('forbidden')
   
def display_message(request):
   if not request.session.get('can_access_display'):
      request.session['can_access_forbidden'] = True
      return redirect('forbidden')
   else:
      del request.session['can_access_display']
      return render(request, 'home/message.html')
   

def not_authenticated(request):
   if not request.session.get('can_access_forbidden'):
      return redirect('welcome')
   else:
      del request.session['can_access_forbidden']
      return render(request, 'home/forbidden.html')