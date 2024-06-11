from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Post, Profile, Message

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

@login_required
def profile(request, username):
    user = User.objects.get(username=username)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your profile has been updated!')
            return redirect('profile', username=user.username)
    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'user': user,
    }
    return render(request, 'profile.html', context)

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
    posts = Post.objects.all()
    return render(request, 'dashboard.html', {'posts': posts})



@login_required
def messages(request):
    user = request.user
    messages_received = Message.objects.filter(receiver=user)
    messages_sent = Message.objects.filter(sender=user)
    return render(request, 'messages.html', {'messages_received': messages_received, 'messages_sent': messages_sent})
