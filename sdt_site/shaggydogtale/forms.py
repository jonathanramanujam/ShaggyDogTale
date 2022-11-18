from django import forms
from .models import Story

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
