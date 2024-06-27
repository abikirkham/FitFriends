from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegisterForm, ProfileForm
from .models import Post, Profile, Message, Comment
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.http import require_POST

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


@login_required
def dashboard(request):
    if request.method == 'POST':
        if 'post_status' in request.POST:
            content = request.POST.get('content', '').strip()
            if content:
                Post.objects.create(content=content, author=request.user)
            else:
                pass

        elif 'post_comment' in request.POST:
            post_id = request.POST.get('post_id')
            content = request.POST.get('content', '').strip()
            if content:
                post = Post.objects.get(id=post_id)
                Comment.objects.create(post=post, content=content, author=request.user)
            else:
                pass

        return redirect('dashboard')
        
    posts = Post.objects.order_by('-created_at')
    return render(request, 'dashboard.html', {'posts': posts})

@require_POST
def like_post(request):
    post_id = request.POST.get('post_id')
    if post_id:
        post = Post.objects.get(id=post_id)
        post.like_count += 1
        post.save()
        return JsonResponse({'status': 'ok', 'like_count': post.like_count})
    return JsonResponse({'status': 'error'})

@require_POST
def dislike_post(request):
    post_id = request.POST.get('post_id')
    if post_id:
        post = Post.objects.get(id=post_id)
        post.dislike_count += 1
        post.save()
        return JsonResponse({'status': 'ok', 'dislike_count': post.dislike_count})
    return JsonResponse({'status': 'error'})

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user == post.author:
        post.delete()
    
    return redirect('profile', username=request.user.username)

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
