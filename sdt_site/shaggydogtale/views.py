from django.shortcuts import render, redirect
from .models import Story, Contribution
from .forms import BeginningForm, MiddleForm, EndForm
from django.contrib import messages
from itertools import chain

# Create your views here.
def Browse(request):
    stories = Story.objects.all()

    context = {
        'stories': stories
    }

    return render(request, 'shaggydogtale/browse.html', context)

def Contributed(request):
    contributions = Contribution.objects.filter(user = request.user)

    context = {
        'contributions': contributions
    }

    return render(request, 'shaggydogtale/contributed.html', context)


def View(request, story_id):
    story = Story.objects.get(id=story_id)

    context = {
        'story': story
    }

    return render(request, 'shaggydogtale/view.html', context)

def Create(request):
    beginningForm = BeginningForm(request.POST or None)

    if beginningForm.is_valid():
        story_id = beginningForm.save()

        Contribution.objects.create(user=request.user, story=story_id, section='b')

        messages.success(request, f'New story saved')
        # redirect to users tales
        return redirect('shaggydogtale:browse')

    context = {
        'beginningForm': beginningForm
    }

    return render(request, 'shaggydogtale/create.html', context)
