from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from home.models import Player

@receiver(post_save, sender = User)
def create_player(sender, instance, created, **kwargs):
    print('signal process')
    if created:
        newPlayer = Player(user = instance, first = instance.first_name, last = instance.last_name, rank = 0)
        newPlayer.save()
        print('new Player made!')
