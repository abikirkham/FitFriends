from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegisterForm
from .models import Post, Profile, Message, Like, Comment

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def about(request):
    return render(request, 'about.html')

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    user_posts = Post.objects.filter(author=user)
    profile = Profile.objects.get(user=user)
    is_friend = profile.friends.filter(id=request.user.id).exists()

    if request.method == 'POST':
        # Update the user's bio if the form is submitted
        bio = request.POST.get('bio')
        profile.bio = bio
        profile.save()
        messages.success(request, 'Your bio has been updated!')

    # Get the profile of the logged-in user
    logged_in_profile = Profile.objects.get(user=request.user)
    
    context = {
        'user': user,
        'user_posts': user_posts,
        'profile': profile,
        'is_friend': is_friend,
        'logged_in_friends': logged_in_profile.friends.all(),
    }
    return render(request, 'profile.html', context)

@login_required
def follow(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    user_profile = Profile.objects.get(user=request.user)
    user_to_follow_profile = Profile.objects.get(user=user_to_follow)
    user_profile.friends.add(user_to_follow)
    user_to_follow_profile.friends.add(request.user)
    return redirect('profile', username=username)

@login_required
def unfollow(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    user_profile = Profile.objects.get(user=request.user)
    user_to_unfollow_profile = Profile.objects.get(user=user_to_unfollow)
    user_profile.friends.remove(user_to_unfollow)
    user_to_unfollow_profile.friends.remove(request.user)
    return redirect('profile', username=username)

@login_required
def dashboard(request):
    if request.method == 'POST':
        if 'post_status' in request.POST:
            title = request.POST.get('title')
            content = request.POST.get('content')
            Post.objects.create(title=title, content=content, author=request.user)
        elif 'post_comment' in request.POST:
            post_id = request.POST.get('post_id')
            content = request.POST.get('content')
            post = Post.objects.get(id=post_id)
            Comment.objects.create(post=post, content=content, author=request.user)
        elif 'like_post' in request.POST:
            post_id = request.POST.get('post_id')
            post = Post.objects.get(id=post_id)
            like, created = Like.objects.get_or_create(post=post, user=request.user)
            if not created:
                like.delete()
        return redirect('dashboard')  # Redirect to the dashboard page after processing the form

    # Fetch posts ordered by creation date in descending order
    posts = Post.objects.order_by('-created_at')
    return render(request, 'dashboard.html', {'posts': posts})

@login_required
def view_messages(request):
    user = request.user
    messages_received = Message.objects.filter(receiver=user)
    messages_sent = Message.objects.filter(sender=user)
    return render(request, 'messages.html', {'messages_received': messages_received, 'messages_sent': messages_sent})
