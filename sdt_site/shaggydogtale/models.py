from django.db import models

# Create your models here.
class Story(models.Model):
    def __str__(self):
        return self.title

    title = models.CharField(max_length=100)
    beginning = models.TextField(max_length=2000)
    middle = models.TextField(max_length=2000)
    end = models.TextField(max_length=2000)
