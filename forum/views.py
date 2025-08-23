from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Category, Discussion, Comment


# home view is completed by me. - {{Utsav CE027}}
def home(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'forum/home.html', context)


# category_discussions view is completed by me. - {{Utsav CE027}}
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

# {{Ronak CE037}} - new_category view is implemented by me.
@login_required(login_url='login')
def new_category(request):
    error_message = None
    if request.method == 'POST':
        category_name = request.POST.get('name', '').strip()
        if Category.objects.filter(name__iexact=category_name).exists():
            error_message = "Category already exists!"
        else:
            Category.objects.create(name=category_name)
            messages.success(request, f"Category '{category_name}' added successfully!")
            return redirect('home')
    context = {
        'categories': Category.objects.all(),
        'error_message': error_message,
    }
    return render(request, 'forum/new_category.html', context)


# discussion_detail view is completed by me. - {{Utsav CE027}}
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

# new_discussion view is completed by me. - {{Utsav CE027}}
@login_required(login_url='login')
def new_discussion(request, category_id=None):
    categories = Category.objects.all()
    selected_category = None
    if category_id:
        selected_category = get_object_or_404(Category, pk=category_id)
    
    if request.method == 'POST':
        form_category_id = request.POST.get('category')
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = get_object_or_404(Category, pk=form_category_id)
        Discussion.objects.create(category=category, title=title, content=content, author=request.user)
        return redirect('category_discussions', category_id=category.id)
    
    context = {
        'categories': categories,
        'selected_category': selected_category,
    }
    return render(request, 'forum/new_discussion.html', context)

# delete_discussion view is completed by me. - {{Utsav CE027}}
@login_required(login_url='login')
def delete_discussion(request, discussion_id):
    discussion = get_object_or_404(Discussion, pk=discussion_id)
    if discussion.author == request.user:
        category_id = discussion.category.id
        discussion.delete()
        messages.success(request, "Discussion deleted successfully.")
        return redirect('category_discussions', category_id=category_id)
    else:
        messages.error(request, "You are not allowed to delete this discussion.")
        return redirect('discussion_detail', discussion_id=discussion_id)


# {{Ronak CE037}} - add_comment view is implemented by me.
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

# {{Ronak CE037}} - delete_comment view is implemented by me.
@login_required(login_url='login')
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.author == request.user:
        discussion_id = comment.discussion.id
        comment.delete()
        messages.success(request, "Comment deleted successfully.")
        return redirect('discussion_detail', discussion_id=discussion_id)
    else:
        messages.error(request, "You are not allowed to delete this comment.")
        return redirect('discussion_detail', discussion_id=comment.discussion.id)


# {{Ronak CE037}} - login_view, logout_view and signup_view is done by me.
def login_view(request):
    categories = Category.objects.all()
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            error_message = "Invalid username or password!"
    context = {
        'categories': categories,
        'error_message': error_message,
    }
    return render(request, 'forum/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')

def signup_view(request):
    categories = Category.objects.all()
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        
        if User.objects.filter(username__iexact=username).exists():
            error_message = "Username already exists!"
        elif User.objects.filter(email__iexact=email).exists():
            error_message = "An account with this email already exists!"
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('home')
    
    context = {
        'categories': categories,
        'error_message': error_message,
    }
    return render(request, 'forum/signup.html', context)


# {{Ronak CE037}} - search function view is done by me.
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


# about view is completed by me. - {{Utsav CE027}}
def about(request):
    return render(request, 'forum/about.html')

