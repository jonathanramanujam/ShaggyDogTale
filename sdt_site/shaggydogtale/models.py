from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Story(models.Model):
    def __str__(self):
        return self.title

    title = models.CharField(max_length=100)
    beginning = models.TextField(max_length=2000)
    middle = models.TextField(max_length=2000)
    end = models.TextField(max_length=2000)

class Contribution(models.Model):
    def __str__(self):
        return f'Story: {self.story} - {self.section}'

    user = models.ForeignKey(User, related_name='contributions', on_delete=models.CASCADE)
    story = models.ForeignKey(Story, related_name='contributions', on_delete=models.CASCADE)
    section = models.CharField(max_length=1) # b = beginning, m = middle, e = end
