from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from .models import Thought, EmotionTag, UserProfile, DraftThought
from .forms import ThoughtForm, UserSignUpForm, UserProfileForm, EmailAuthenticationForm

def landing_page(request):
    emotion_tags = EmotionTag.objects.all()
    if request.method == 'POST':
        form = ThoughtForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                thought = form.save(commit=False)
                thought.author = request.user
                thought.save()
                messages.success(request, 'Your thought has been shared!')
                return redirect('feed')
            else:
                # Store draft thought in session
                draft = DraftThought.objects.create(
                    content=form.cleaned_data['content'],
                    emotion_tag=form.cleaned_data.get('emotion_tag'),
                    session_key=request.session.session_key or request.session.create()
                )
                request.session['draft_thought_id'] = draft.id
                return redirect('signup')
    else:
        form = ThoughtForm()
    
    return render(request, 'thoughtify/index.html', {
        'form': form,
        'emotion_tags': emotion_tags
    })

def signup_view(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile with anonymous code
            UserProfile.objects.create(
                user=user,
                anonymous_code=UserProfile.generate_anonymous_code(user.username)
            )
            login(request, user)
            
            # Check for draft thought
            draft_id = request.session.get('draft_thought_id')
            if draft_id:
                try:
                    draft = DraftThought.objects.get(id=draft_id)
                    draft.publish(user)
                    del request.session['draft_thought_id']
                    messages.success(request, 'Your thought has been published!')
                except DraftThought.DoesNotExist:
                    pass
            
            return redirect('feed')
    else:
        form = UserSignUpForm()
    
    return render(request, 'thoughtify/signup.html', {'form': form})

@login_required
def feed(request):
    user_profile = request.user.userprofile
    thoughts = Thought.objects.select_related('author__userprofile', 'emotion_tag')
    
    # Filter thoughts based on user preferences
    if not user_profile.show_public_thoughts:
        thoughts = thoughts.filter(author=request.user)
    else:
        thoughts = thoughts.filter(
            Q(author=request.user) | Q(is_public=True)
        )
    
    # Check for daily thought nudge
    show_daily_nudge = user_profile.can_post_daily_thought()
    
    paginator = Paginator(thoughts, 20)
    page = request.GET.get('page', 1)
    thoughts_page = paginator.get_page(page)
    
    if request.headers.get('HX-Request'):
        # Return only thought list for infinite scroll
        return render(request, 'thoughtify/partials/thought_list.html', {
            'thoughts': thoughts_page
        })
    
    emotion_tags = EmotionTag.objects.all()
    return render(request, 'thoughtify/feed.html', {
        'thoughts': thoughts_page,
        'emotion_tags': emotion_tags,
        'show_daily_nudge': show_daily_nudge
    })

@login_required
def create_thought(request):
    is_daily_thought = request.POST.get('is_daily_thought') == 'true'
    
    if request.method == 'POST':
        form = ThoughtForm(request.POST)
        if form.is_valid():
            thought = form.save(commit=False)
            thought.author = request.user
            
            if is_daily_thought:
                if not request.user.userprofile.can_post_daily_thought():
                    messages.error(request, "You've already posted your daily thought")
                    return redirect('feed')
                thought.is_daily_thought = True
                request.user.userprofile.last_daily_thought = timezone.now().date()
                request.user.userprofile.save()
            
            thought.save()
            messages.success(request, 'Your thought has been shared!')
            
            if request.headers.get('HX-Request'):
                return render(request, 'thoughtify/partials/thought.html', {
                    'thought': thought
                })
            return redirect('feed')
    else:
        form = ThoughtForm()
    
    context = {
        'form': form,
        'is_daily_thought': is_daily_thought,
        'emotion_tags': EmotionTag.objects.all()
    }
    return render(request, 'thoughtify/create_thought.html', context)

@login_required
def update_thought(request, thought_id):
    thought = get_object_or_404(Thought, id=thought_id, author=request.user)
    if request.method == 'POST':
        form = ThoughtForm(request.POST, instance=thought)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your thought has been updated!')
            return redirect('feed')
    else:
        form = ThoughtForm(instance=thought)
    
    return render(request, 'thoughtify/update_thought.html', {
        'form': form,
        'thought': thought
    })

@login_required
def delete_thought(request, thought_id):
    thought = get_object_or_404(Thought, id=thought_id, author=request.user)
    if request.method == 'POST':
        thought.delete()
        messages.success(request, 'Your thought has been deleted.')
        if request.headers.get('HX-Request'):
            return JsonResponse({'success': True})
        return redirect('feed')
    
    return render(request, 'thoughtify/delete_thought.html', {'thought': thought})

@login_required
def toggle_public_thoughts(request):
    if request.method == 'POST':
        profile = request.user.userprofile
        profile.show_public_thoughts = not profile.show_public_thoughts
        profile.save()
        return redirect('feed')
