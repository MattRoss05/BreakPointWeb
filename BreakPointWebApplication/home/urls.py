from django.urls import path
from . import views


urlpatterns = [
    path('', views.welcome_page, name = 'welcome'),
    path('about', views.about_page, name = 'about'),
    
]
