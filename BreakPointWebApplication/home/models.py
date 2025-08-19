from django.db import models
from django.contrib.auth.models import User
class Player(models.Model):
    user = models.OneToOneField(User, on_delete= models.PROTECT)
    first = models.CharField(max_length=50)
    last = models.CharField(max_length=50)
    rank  = models.IntegerField()
    matches = models.IntegerField(default = 0)
    wins = models.IntegerField(default = 0)
    def __str__(self):
        return self.first + " " + self.last


class Match(models.Model):

    player1 = models.ForeignKey(Player, on_delete=models.PROTECT, related_name='matches_as_player1')

    player2 = models.ForeignKey(Player, on_delete=models.PROTECT, related_name='matches_as_player2')

    match_type = models.CharField(max_length=9)

    winner = models.ForeignKey(Player, on_delete=models.PROTECT, related_name= 'matches_won')
    def __str__(self):
        return f"{self.player1} vs {self.player2} ({self.match_type})"