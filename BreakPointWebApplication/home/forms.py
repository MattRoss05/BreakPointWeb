
from django import forms
from .models import Match, Player
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate

class MatchForm(forms.ModelForm):
    #list of active players
    OPPONENT_CHOICES = Player.objects.all()
    #Types of matches
    MATCH_TYPE_CHOICES = [
        ("Race to 2","Race to 2"),
        ("Race to 3","Race to 3"),
        ("Race to 5","Race to 5"),
    ]
    #Yes or no choices
    WIN_CHOICES = [
        ("Yes","Yes"),
        ("No","No")
    ]
    #opponent list
    opponent = forms.ModelChoiceField(required = True, queryset=OPPONENT_CHOICES)
    #type of match played
    match_type = forms.ChoiceField(required = True, choices=MATCH_TYPE_CHOICES)
    #Did you win?
    win = forms.ChoiceField(required = True, choices= WIN_CHOICES)
    #The oponents password so both parties must consent to a ranked match
    opponent_password = forms.CharField(
        widget=forms.PasswordInput(),
        max_length=100,
        help_text="Have your opponent enter their password."
    )
    class Meta:
        #model being created
        model = Match

        fields= [
            #specify order and which model fields to appear on the form
            "opponent",
            "match_type",
            "win",
            "opponent_password",

        ]
    # override init function. 
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if self.user:
            # get the player model associated with the logged in user
            player = Player.objects.get(user=self.user)
            # return the list of active players excluding the retrieved player model
            self.fields["opponent"].queryset = Player.objects.filter(user__is_active = True).exclude(pk=player.pk).order_by('first')
    
    def clean_opponent_password(self):
        # get opponent chosed
        opponent = self.cleaned_data.get('opponent')
        #get password typed in the form
        opponent_password = self.cleaned_data.get('opponent_password')
        # if the password isn't the correct password associated with the oponent
        if not check_password(opponent_password, opponent.user.password):
            #raise a form error
            raise forms.ValidationError("Incorrect Opponent Password")
        #return the typed password if everything matches
        return opponent_password
    
    #override save
    def save(self, commit = True):
        #call save from parent class to create a match model instance but do not commit the changes to the database
        match = super().save(commit = False)
        #player1 = user that submitted the form
        match.player1 = Player.objects.get(user = self.user)
        #player2 = oponent chosen
        match.player2 = self.cleaned_data.get('opponent')
        # match type = type chosen
        match.match_type = self.cleaned_data.get('match_type')
        #find out who is the winner based off of yes no answer
        if self.cleaned_data.get('win') == 'Yes':
            match.winner = match.player1
            match.player1.wins += 1

        else:
            match.winner = match.player2
            match.player2.wins += 1
        # if commit is not specifies in fuction arguments or specified as true
        if commit:
            match.save()
            #get expected win probabilities for both players
            expected_1 = exp_win1(match.player1, match.player2)
            expected_2 = 1 - expected_1
            #get proper k factors for both players
            kfact1 = get_kfactor(match.player1, match)
            kfact2 = get_kfactor(match.player2, match)
            #distribute points
            if match.winner == match.player1: 
                match.player1.rank = match.player1.rank + kfact1 * (1 - expected_1)
                match.player2.rank = match.player2.rank + kfact2 * (0 - expected_2)
            else:
                match.player2.rank = match.player2.rank + kfact2 * (1 - expected_2)
                match.player1.rank = match.player1.rank + kfact1 * (0 - expected_1)
            #increment matches played for both players
            match.player1.matches  += 1
            match.player2.matches  += 1
            #save the player models and commit changes to the database
            match.player1.save()
            match.player2.save()
        #return match created
        return match
#multipliers to variable in elo equation determining elo gain/loss
def kfactor_mult(match):
    if match.match_type == "Race to 2":
        return 1
    elif match.match_type == "Race to 3":
        return 1.25
    else:
        return 1.5
#variable from elo equation affected by number of matches a player has played. imbedded use of kfactor_mult function
#to determine multiplier added
def get_kfactor(player, match): 
    if player.matches <= 2:
        return 48 * kfactor_mult(match)
    elif player.matches <= 4:
        return 40 * kfactor_mult(match)
    elif player.matches <=7:
        return 32 * kfactor_mult(match)
    elif player.matches <=14:
        return 24 * kfactor_mult(match)
    else:
        return 16 * kfactor_mult(match)
#probability equation to determine the probabiltiy of a given players chance of win
def exp_win1(player1,player2):
    denom = 1 + 10**((player2.rank - player1.rank)/400)
    exp = 1/denom
    return exp
class LeaveForm(forms.Form):
    #enter password twice
    password1 = forms.CharField(max_length=100, widget=forms.PasswordInput(), help_text='Enter your password')
    password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(), help_text='Confirm Password')
    #Need to override init function to pass user to the clean method below
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
    #override cleam
    def clean(self):
        #get cleaned data
        cleaned_data = super().clean()
        pw1 = cleaned_data.get('password1')
        pw2 = cleaned_data.get('password2')
        # if the password don't match, raise a form error
        if pw1 != pw2:
            raise forms.ValidationError('Passwords do not match.')
        #if the password does not match the user authenticated
        if not authenticate(username = self.user.username, password = pw1):
            # raise a form error
            raise forms.ValidationError('Incorrect password.')
        #return the cleaned data
        return cleaned_data

