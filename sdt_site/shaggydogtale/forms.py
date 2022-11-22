from django import forms
from .models import Story, Vote

class BeginningForm(forms.ModelForm):
    beginning = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10,}), label='')
    class Meta:
        model = Story
        fields = ["title", "beginning"]

class MiddleForm(forms.ModelForm):
    middle = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), label='')
    class Meta:
        model = Story
        fields = ["middle"]

class EndForm(forms.ModelForm):
    end = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), label='')
    class Meta:
        model = Story
        fields = ["end"]
