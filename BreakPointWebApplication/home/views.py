from django.shortcuts import render, redirect
from .models import Player
from .forms import MatchForm
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


def match_page(request):
   if request.method == "POST":
      form = MatchForm(request.POST, user = request.user)
      if form.is_valid():
         form.save()
         return redirect('welcome')
   else:
      form = MatchForm(user = request.user)
   return render(request, 'home/match.html', {'form': form})

