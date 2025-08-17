from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
  path('logout_user/', views.logout_user, name = 'logout'),
  path('join/', views.register_user, name = 'join'),

]