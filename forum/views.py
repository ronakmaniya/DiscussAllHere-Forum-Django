from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Category, Discussion, Comment

def home(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'forum/home.html', context)

def category_discussions(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    discussions = category.discussions.all().order_by('-created_at')
    categories = Category.objects.all()
    context = {
        'category': category,
        'discussions': discussions,
        'categories': categories,
    }
    return render(request, 'forum/category_discussions.html', context)

def discussion_detail(request, discussion_id):
    discussion = get_object_or_404(Discussion, pk=discussion_id)
    comments = discussion.comments.filter(parent__isnull=True).order_by('created_at')
    categories = Category.objects.all()
    context = {
        'discussion': discussion,
        'comments': comments,
        'categories': categories,
    }
    return render(request, 'forum/discussion_detail.html', context)

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
    context = {
        'categories': categories,
    }
    return render(request, 'forum/new_discussion.html', context)

@login_required(login_url='login')
def add_comment(request, discussion_id):
    discussion = get_object_or_404(Discussion, pk=discussion_id)
    if request.method == 'POST':
        text = request.POST.get('text')
        parent_id = request.POST.get('parent')
        parent = get_object_or_404(Comment, pk=parent_id) if parent_id else None
        Comment.objects.create(
            discussion=discussion,
            author=request.user,
            text=text,
            parent=parent
        )
        return redirect('discussion_detail', discussion_id=discussion_id)
    return redirect('discussion_detail', discussion_id=discussion_id)

def login_view(request):
    categories = Category.objects.all()
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
    context = {
        'categories': categories,
    }
    return render(request, 'forum/login.html', context)

def signup(request):
    categories = Category.objects.all()
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
    context = {
        'categories': categories,
    }
    return render(request, 'forum/signup.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')

def search(request):
    query = request.GET.get('q')
    discussions = Discussion.objects.filter(title__icontains=query)
    categories = Category.objects.all()
    context = {
        'discussions': discussions,
        'query': query,
        'categories': categories,
    }
    return render(request, 'forum/search_results.html', context)

def about(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'forum/about.html', context)

