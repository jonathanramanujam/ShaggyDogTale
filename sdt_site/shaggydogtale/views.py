from django.shortcuts import render
from .models import Story

# Create your views here.
def Browse(request):
    stories = Story.objects.all()

    context = {
        'stories': stories
    }

    return render(request, 'shaggydogtale/browse.html', context)

def View(request, story_id):
    story = Story.objects.get(id=story_id)

    context = {
        'story': story
    }

    return render(request, 'shaggydogtale/view.html', context)
