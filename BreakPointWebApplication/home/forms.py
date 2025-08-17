from django import forms
from .models import Match, Player
from django.contrib.auth.hashers import check_password
class MatchForm(forms.ModelForm):
    OPPONENT_CHOICES = Player.objects.all()
    MATCH_TYPE_CHOICES = [
        ("Race to 2","Race to 2"),
        ("Race to 3","Race to 3"),
        ("Race to 5","Race to 5"),
    ]
    WIN_CHOICES = [
        ("Yes","Yes"),
        ("No","No")
    ]
    opponent = forms.ModelChoiceField(required = True, queryset=OPPONENT_CHOICES)
    match_type = forms.ChoiceField(required = True, choices=MATCH_TYPE_CHOICES)
    win = forms.ChoiceField(required = True, choices= WIN_CHOICES)
    opponent_password = forms.CharField(max_length=100, help_text= "Have your opponent enter their password.")
    class Meta:

        model = Match

        fields= [
            "opponent",
            "match_type",
            "win",
            "opponent_password",

        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        player = Player.objects.get(user=self.user)
        self.fields["opponent"].queryset = Player.objects.exclude(pk=player.pk)
    
    def clean_opponent_password(self):
        opponent = self.cleaned_data.get('opponent')
        opponent_password = self.cleaned_data.get('opponent_password')
        if not check_password(opponent_password, opponent.user.password):
            raise forms.ValidationError("Incorrect Opponent Password")
        
        return opponent_password
    def save(self, commit = True):
        match = super().save(commit = False)
        match.player1 = Player.objects.get(user = self.user)

        match.player2 = self.cleaned_data.get('opponent')

        match.match_type = self.cleaned_data.get('match_type')

        if self.cleaned_data.get('win') == 'Yes':
            match.winner = match.player1

        else:
            match.winner = match.player2

        if commit:
            match.save()

            match.player1.matches  = match.player1.matches + 1
            match.player2.matches  = match.player2.matches + 1
            match.player1.save()
            match.player2.save()
        
        return match


