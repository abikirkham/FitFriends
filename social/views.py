from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import DetailView
from django.views import View
from django.db.models import Q

from .forms import UserRegisterForm, ProfileForm, CommentForm
from .models import Post, Profile, Message, Like


def like_view(request):
    if request.method == 'POST' and request.user.is_authenticated:
        liked_post_id = request.POST.get('post_id')
        liked_post = get_object_or_404(Post, id=liked_post_id)
        like, created = Like.objects.get_or_create(user=request.user, liked_post=liked_post)
        if not created:
            like.delete()
            return JsonResponse({'liked': False, 'like_count': liked_post.like_set.count()})
        else:
            return JsonResponse({'liked': True, 'like_count': liked_post.like_set.count()})
    return JsonResponse({}, status=400)


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

def home(request):
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

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    user_posts = Post.objects.filter(author=user)
    profile = Profile.objects.get(user=user)
    is_friend = profile.friends.filter(id=request.user.id).exists()

    if request.method == 'POST':
        bio = request.POST.get('bio', '')
        profile.bio = bio
        if 'image' in request.FILES:
            profile.image = request.FILES['image']
        profile.save()
        messages.success(request, 'Your profile has been updated!')

    logged_in_profile = Profile.objects.get(user=request.user)
    
    context = {
        'user': user,
        'user_posts': user_posts,
        'profile': profile,
        'is_friend': is_friend,
        'logged_in_friends': logged_in_profile.friends.all(),
    }
    return render(request, 'profile.html', context)

def profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile.html', {'form': form, 'profile': profile})

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

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user == post.author:
        post.delete()
    
    return redirect('profile', username=request.user.username)

@login_required
def dashboard(request):
    if request.method == 'POST':
        if 'post_status' in request.POST:
            content = request.POST.get('content', '').strip()
            if content:
                Post.objects.create(content=content, author=request.user)
            return redirect('dashboard')
        
        if 'comment_post' in request.POST:
            post_id = request.POST.get('post_id')
            comment_form = CommentForm(request.POST)
            post = get_object_or_404(Post, id=post_id)
            if comment_form.is_valid():
                comment_form.instance.email = request.user.email
                comment_form.instance.name = request.user.username
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.approved = True
                comment.save()
                return redirect('dashboard')

    posts = Post.objects.order_by('-created_at')
    comment_form = CommentForm()

    posts_with_comments = []
    for post in posts:
        comments = post.comments.filter(approved=True).order_by("-created_on")
        posts_with_comments.append((post, comments))

    return render(request, 'dashboard.html', {'posts_with_comments': posts_with_comments, 'comment_form': comment_form})


@login_required
def view_messages(request):
    user = request.user
    selected_username = request.GET.get('username')
    
    if selected_username:
        selected_friend = get_object_or_404(User, username=selected_username)
        conversation = Message.objects.filter(
            Q(sender=user, receiver=selected_friend) | Q(sender=selected_friend, receiver=user)
        ).order_by('created_at')
    else:
        selected_friend = None
        conversation = []

    friends = user.profile.friends.all()
    context = {
        'user': user,
        'friends': friends,
        'selected_friend': selected_friend,
        'conversation': conversation,
    }
    return render(request, 'messages.html', context)

@login_required
def send_message(request):
    if request.method == 'POST':
        receiver_username = request.POST.get('receiver')
        receiver = get_object_or_404(User, username=receiver_username)
        content = request.POST.get('content')
        
        if content:
            message = Message.objects.create(sender=request.user, receiver=receiver, content=content)
            return JsonResponse({
                'success': True,
                'message': message.content,
                'timestamp': message.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'sender': message.sender.username,
                'sender_name': message.sender.username
            })
        
    return JsonResponse({'success': False})

