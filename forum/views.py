from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Discussion
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def home(request):
    # Render different home pages based on login status
    if request.user.is_authenticated:
        return render(request, 'forum/home_loggedin.html', {'user': request.user})
    else:
        return render(request, 'forum/home_not_loggedin.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Check if the username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')
        else:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('home')
    return render(request, 'forum/signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')
    return render(request, 'forum/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def discussion_list(request):
    discussions = Discussion.objects.all().order_by('-created_at')
    return render(request, 'forum/discussion_list.html', {'discussions': discussions})

def discussion_detail(request, discussion_id):
    discussion = get_object_or_404(Discussion, pk=discussion_id)
    return render(request, 'forum/discussion_detail.html', {'discussion': discussion})

@login_required(login_url='login')
def new_discussion(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        Discussion.objects.create(title=title, content=content, author=request.user)
        return redirect('discussion_list')
    return render(request, 'forum/new_discussion.html')
