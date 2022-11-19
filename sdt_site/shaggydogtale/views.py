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
    contributions = story.contributions.all()
    #Attempt to get the user contribution
    try:
        userContribution = contributions.get(user=request.user)
    except:
        userContribution = None
    message=None
    form=None

    # If the current user is a contributor
    if userContribution:
        message='User Contributed'
        # if contribution is beginning, add beginningform
        if userContribution.section == 'b':
            message+=' Beginning'
            form = BeginningForm(request.POST or None, instance=story)
            if form.is_valid():
                form.save()
        # elseif contribution is middle, add middleform
        if userContribution.section == 'm':
            message+=' Middle'
            form = MiddleForm(request.POST or None, instance=story)
            if form.is_valid():
                form.save()
        # elseif contribution is end, add endform
        if userContribution.section == 'e':
            message+=' End'
            form = EndForm(request.POST or None, instance=story)
            if form.is_valid():
                form.save()

    # Else, the current user has not contributed to the story
    else:
        message="User did not contribute"
        # if middle has not been written, show middleform

        # elseif end has not been written, show endform
        # else, the story is complete, just display.

    context = {
        'story': story,
        'contributions': contributions,
        'userContribution': userContribution,
        'message': message,
        'form': form
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
