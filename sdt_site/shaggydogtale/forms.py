from django import forms
from .models import Story, Vote

class BeginningForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ["title", "beginning"]

class MiddleForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ["middle"]

class EndForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ["end"]

class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ["user", "story", "vote"]
