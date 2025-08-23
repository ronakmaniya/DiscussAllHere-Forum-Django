from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Category, Discussion, Comment

def home(request):
    categories = Category.objects.all()
    return render(request, 'forum/home.html', {'categories': categories})

def category_discussions(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    discussions = category.discussions.all().order_by('-created_at')
    return render(request, 'forum/category_discussions.html', {
        'category': category,
        'discussions': discussions
    })

def discussion_detail(request, discussion_id):
    discussion = get_object_or_404(Discussion, pk=discussion_id)
    comments = discussion.comments.filter(parent__isnull=True).order_by('created_at')
    return render(request, 'forum/discussion_detail.html', {
        'discussion': discussion,
        'comments': comments
    })

@login_required(login_url='login')
def new_discussion(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        category_id = request.POST.get('category')
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = get_object_or_404(Category, pk=category_id)
        Discussion.objects.create(category=category, title=title, content=content, author=request.user)
        return redirect('category_discussions', category_id=category.id)
    return render(request, 'forum/new_discussion.html', {'categories': categories})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')
    return render(request, 'forum/login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('home')
    return render(request, 'forum/signup.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def search(request):
    query = request.GET.get('q')
    discussions = Discussion.objects.filter(title__icontains=query)
    return render(request, 'forum/search_results.html', {'discussions': discussions, 'query': query})
