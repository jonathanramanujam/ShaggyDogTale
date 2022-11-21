from django.shortcuts import render, redirect
from .models import Story, Contribution, User, Vote
from .forms import BeginningForm, MiddleForm, EndForm
from django.contrib import messages

# Create your views here.
def Browse(request):
    stories = Story.objects.all()

    context = {
        'stories': stories
    }

    return render(request, 'shaggydogtale/browse.html', context)

def Contributed(request, user_id=None):
    title = None
    if user_id == None:
        contributions = Contribution.objects.filter(user = request.user)
        title = 'Your Tales'
    else:
        user = User.objects.get(id=user_id)
        contributions = Contribution.objects.filter(user = user)
        title = f'{user.username}\'s Tales'

    context = {
        'title': title,
        'contributions': contributions
    }

    return render(request, 'shaggydogtale/contributed.html', context)


def View(request, story_id):
    story = Story.objects.get(id=story_id)

    contributions = story.contributions.all()
    userContribution = None
    beginningContributor = None
    middleContributor = None
    endContributor = None
    beginningContributorRating = 0
    middleContributorRating = 0
    endContributorRating = 0
    userVote = None

    for contribution in contributions:
        # Check if this is the current user's contribution
        if contribution.user == request.user:
            userContribution = contribution

        # Get the usernames of contributors for each section
        match contribution.section:
            case 'b':
                beginningContributor = User.objects.get(id=contribution.user.id)
                for contribution in beginningContributor.contributions.all():
                    for vote in contribution.story.votes.all():
                        beginningContributorRating += vote.vote
            case 'm':
                middleContributor = User.objects.get(id=contribution.user.id)
                for contribution in middleContributor.contributions.all():
                    for vote in contribution.story.votes.all():
                        middleContributorRating += vote.vote
            case 'e':
                endContributor = User.objects.get(id=contribution.user.id)
                for contribution in endContributor.contributions.all():
                    for vote in contribution.story.votes.all():
                        endContributorRating += vote.vote

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
                return redirect('shaggydogtale:view', story_id=story.id)
        # elseif end has not been written, show endform
        elif contributions.count() == 2:
            form = EndForm(request.POST or None, instance=story)
            if form.is_valid():
                story_id = form.save()
                Contribution.objects.create(user=request.user, story=story_id, section='e')
                messages.success(request, f'End created for {story.title}!')
                return redirect('shaggydogtale:view', story_id=story.id)
        # otherwise, the story is complete and can be voted on
        else:
            # storyVotes = Vote.objects.filter(story=story_id)
            userVote = Vote.objects.filter(user=request.user, story=story_id)
            if userVote.count() == 0:
                if 'Upvote' in request.POST:
                    Vote.objects.create(user=request.user, story=story, vote=1)
                    messages.success(request, f'Upvoted {story.title}!')
                    return redirect('shaggydogtale:view', story_id=story.id)
                if 'Downvote' in request.POST:
                    Vote.objects.create(user=request.user, story=story, vote=-1)
                    messages.success(request, f'Downvoted {story.title}!')
                    return redirect('shaggydogtale:view', story_id=story.id)

    storyRating = 0
    for vote in story.votes.all():
        storyRating += vote.vote

    context = {
        'story': story,
        'contributions': contributions,
        'userContribution': userContribution,
        'beginningContributor': beginningContributor,
        'middleContributor': middleContributor,
        'endContributor': endContributor,
        'beginningContributorRating': beginningContributorRating,
        'middleContributorRating': middleContributorRating,
        'endContributorRating': endContributorRating,
        'message': message,
        'form': form,
        'userVote': userVote,
        'storyRating': storyRating
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
