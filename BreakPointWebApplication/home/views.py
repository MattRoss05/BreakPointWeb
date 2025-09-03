#import needed built in functions and needed models
from django.shortcuts import render, redirect, get_object_or_404
from .models import Player, Match
from .forms import MatchForm, LeaveForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User


def welcome_page(request):
   #render the welcome page
   return render(request, 'home/home.html')

def display_rank(request):
   #if the user is authenticated
   if request.user.is_authenticated:
      #provide user's match data and the VCU rankings

      #get list of players that can be ranked(must have at least five matches)
      player_list = Player.objects.filter(matches__gte = 5, user__is_active = True).order_by('-rank')
      #get player model associated with logged in user
      player = get_object_or_404(Player, user = request.user)
      if player.matches == 0:
         win_ratio = 0
      else:
         #calculate win rate
         win_ratio = round((player.wins/player.matches),2)
      #initialize context dictionary
      context = {
      'player_list' : player_list,
      'player_rating' : player.rank,
      'win_count' : player.wins,
      'loss_count' : (player.matches-player.wins),
      'win_ratio' : win_ratio,

      
      }
      #render the rankings page
      return render(request, 'home/rankings.html', context)
   else:
      #otherwise only display current rankings
      player_list = Player.objects.filter(matches__gte = 5, user__is_active = True).order_by('-rank')
      context = {
         'player_list' : player_list,
      }
      return render(request, 'home/rankings.html', context)


def about_page(request):
   #render the about page
   return render(request, 'home/about.html')


def match_page(request):
   #if the user is authenticated
   if request.user.is_authenticated:
      #if the form has been submitted
      if request.method == "POST":
         #instantiate the form and initialize it
         form = MatchForm(request.POST, user = request.user)
         #if the form is valid
         if form.is_valid():
            #save it
            form.save()
            #redirect user to success page using session variables
            request.session['can_access_display'] = True
            return redirect('message')
      else:
         #otherwise render the match page with an empty form
         form = MatchForm(user = request.user)
      return render(request, 'home/match.html', {'form': form})
   #otherwise redirect to user to the error page using session variables.
   else:
      request.session['can_access_forbidden'] = True
      return redirect('forbidden')
   
 #view function for the match success submission page
def display_message(request):
   if not request.session.get('can_access_display'):
      request.session['can_access_forbidden'] = True
      return redirect('forbidden')
   else:
      del request.session['can_access_display']
      return render(request, 'home/message.html')
   
#view functions that allow users to leave the website. Keeps their data for storing matches and preserving match history
def leave_ranks(request):
   if request.user.is_authenticated:
      if request.method == "POST":
         form = LeaveForm(request.user, request.POST)
         if form.is_valid():
            request.user.is_active = False
            request.user.save()
            return redirect('welcome')
      else:
         form = LeaveForm(request.user)
      return render(request, 'home/leave.html', {'form': form} )
   else:
      request.session['can_access_forbidden'] = True
      return redirect('forbidden')
   

#view function for the forbidded page message page
def not_authenticated(request):
   if not request.session.get('can_access_forbidden'):
      return redirect('welcome')
   else:
      del request.session['can_access_forbidden']
      return render(request, 'home/forbidden.html')