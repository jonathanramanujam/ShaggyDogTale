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
        # if contribution is beginning, add beginningform
        if userContribution.section == 'b':
            form = BeginningForm(request.POST or None, instance=story)
            if form.is_valid():
                form.save()
                messages.success(request, f'Beginning updated for {story.title}!')
        # elseif contribution is middle, add middleform
        elif userContribution.section == 'm':
            form = MiddleForm(request.POST or None, instance=story)
            if form.is_valid():
                form.save()
                messages.success(request, f'Middle updated for {story.title}!')
        # elseif contribution is end, add endform
        elif userContribution.section == 'e':
            form = EndForm(request.POST or None, instance=story)
            if form.is_valid():
                form.save()
                messages.success(request, f'End updated for {story.title}!')

    # Else, the current user has not contributed to the story
    else:
        # if middle has not been written, show middleform
        if contributions.count() == 1:
            form = MiddleForm(request.POST or None, instance=story)
            if form.is_valid():
                story_id = form.save()
                Contribution.objects.create(user=request.user, story=story_id, section='m')
                messages.success(request, f'Middle created for {story.title}!')
        # elseif end has not been written, show endform
        elif contributions.count() == 2:
            form = EndForm(request.POST or None, instance=story)
            if form.is_valid():
                story_id = form.save()
                Contribution.objects.create(user=request.user, story=story_id, section='e')
                messages.success(request, f'End created for {story.title}!')
        # else, the story is complete, just display.
        else:
            message='Story complete'


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
