from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from .models import Thought, EmotionTag, UserProfile, DraftThought, Like
from .forms import ThoughtForm, UserSignUpForm, UserProfileForm, EmailAuthenticationForm
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.views.decorators.http import require_POST

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
            user = form.save(commit=False)
            user.is_active = True  # Activate account immediately
            user.save()
            # Create user profile with anonymous code
            profile = UserProfile.objects.create(
                user=user,
                anonymous_code=UserProfile.generate_anonymous_code(user.username),
            )
            profile.email_confirmed = True  # Mark as confirmed
            profile.confirmation_token = ''
            profile.save()
            messages.success(request, 'Account created! You can now log in.')
            return redirect('login')
    else:
        form = UserSignUpForm()
    return render(request, 'thoughtify/signup.html', {'form': form})

# Remove confirm_email view as it's no longer needed

@login_required
def my_thoughts_view(request):
    user_profile = request.user.userprofile
    thoughts = Thought.objects.filter(author=request.user).select_related('author__userprofile', 'emotion_tag')
    paginator = Paginator(thoughts, 20)
    page = request.GET.get('page', 1)
    thoughts_page = paginator.get_page(page)
    return render(request, 'thoughtify/my_thoughts.html', {
        'thoughts': thoughts_page,
        'user_profile': user_profile,
    })

@login_required
def feed(request):
    user_profile = request.user.userprofile
    thoughts = Thought.objects.select_related('author__userprofile', 'emotion_tag').filter(is_public=True)
    # Feed now only shows public thoughts
    show_daily_nudge = user_profile.can_post_daily_thought()
    paginator = Paginator(thoughts, 20)
    page = request.GET.get('page', 1)
    thoughts_page = paginator.get_page(page)
    if request.headers.get('HX-Request'):
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
            # Return an empty response with 200 status for HTMX
            from django.http import HttpResponse
            return HttpResponse(status=200)
        return redirect('feed')
    
    return render(request, 'thoughtify/delete_thought.html', {'thought': thought})

@login_required
def toggle_public_thoughts(request):
    if request.method == 'POST':
        profile = request.user.userprofile
        profile.show_public_thoughts = not profile.show_public_thoughts
        profile.save()
        return redirect('feed')

def login_view(request):
    from .forms import EmailAuthenticationForm
    form = EmailAuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                request.session['saved_email'] = email
                request.session['saved_password'] = password
                messages.success(request, 'Login successful!')
                return redirect('feed')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        initial = {}
        if 'saved_email' in request.session:
            initial['username'] = request.session['saved_email']
        if 'saved_password' in request.session:
            initial['password'] = request.session['saved_password']
        form = EmailAuthenticationForm(request, initial=initial)
    return render(request, 'thoughtify/login.html', {'form': form})

@login_required
def profile_view(request):
    user = request.user
    profile = user.userprofile
    context = {
        'username': user.username,
        'real_name': f'{user.first_name} {user.last_name}'.strip(),
        'profile': profile,
        'user': user,
    }
    return render(request, 'thoughtify/profile.html', context)

@require_POST
@login_required
def like_thought(request, thought_id):
    thought = get_object_or_404(Thought, id=thought_id)
    like, created = Like.objects.get_or_create(user=request.user, thought=thought)
    if not created:
        # If already liked, unlike
        like.delete()
    # Redirect back to the page the user came from
    return redirect(request.META.get('HTTP_REFERER', 'feed'))
