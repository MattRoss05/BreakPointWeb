from django.db import models
from django.contrib.auth.models import User
class Player(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    first = models.CharField(max_length=50)
    last = models.CharField(max_length=50)
    rank  = models.IntegerField()
    def __str__(self):
        return self.first + " " + self.last + self.user.email


class Match(models.Model):
    MATCH_TYPE_CHOICES = [
        ("Race to 2","Race to 2"),
        ("Race to 3","Race to 3"),
        ("Race to 5","Race to 5"),
    ]

    player1 = models.ForeignKey(Player, on_delete=models.SET_NULL, null = True, related_name='matches_as_player1')

    player2 = models.ForeignKey(Player, on_delete=models.SET_NULL, null = True, related_name='matches_as_player2')

    match_type = models.CharField(choices=MATCH_TYPE_CHOICES, max_length=9)

    winner = models.ForeignKey(Player, on_delete=models.SET_NULL, null = True, related_name= 'matches_won')
    def __str__(self):
        return f"{self.player1} vs {self.player2} ({self.match_type})"