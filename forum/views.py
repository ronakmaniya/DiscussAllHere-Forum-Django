from datetime import timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.utils import timezone

from .models import Category, Discussion, Comment


TOP_CATEGORY_LIMIT = 5


def get_top_categories():
    cutoff = timezone.now() - timedelta(days=30)
    recent = (
        Category.objects
        .annotate(recent_count=Count('discussions', filter=Q(discussions__created_at__gte=cutoff)))
        .filter(recent_count__gt=0)
        .order_by('-recent_count', 'name')
    )
    top_recent = list(recent[:TOP_CATEGORY_LIMIT])
    if len(top_recent) < TOP_CATEGORY_LIMIT:
        remaining = TOP_CATEGORY_LIMIT - len(top_recent)
        recent_ids = [category.id for category in top_recent]
        fallback = (
            Category.objects
            .exclude(id__in=recent_ids)
            .annotate(total_count=Count('discussions'))
            .order_by('-total_count', 'name')
        )
        top_recent.extend(list(fallback[:remaining]))
    return top_recent


def base_context():
    return {
        'top_categories': get_top_categories(),
    }


# home view is completed by me. - {{Utsav CE027}}
def home(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        **base_context(),
    }
    return render(request, 'forum/home.html', context)


def discussion_list(request):
    discussions = Discussion.objects.select_related('category', 'author').all()
    sort = request.GET.get('sort', 'newest')
    category_slug = request.GET.get('category')
    mine = request.GET.get('mine') == '1'

    if category_slug:
        discussions = discussions.filter(category__slug=category_slug)
    if mine and request.user.is_authenticated:
        discussions = discussions.filter(author=request.user)

    if sort == 'oldest':
        discussions = discussions.order_by('created_at')
    else:
        discussions = discussions.order_by('-created_at')

    paginator = Paginator(discussions, 10)
    page_obj = paginator.get_page(request.GET.get('page', 1))
    categories = Category.objects.all()
    context = {
        'discussions': page_obj,
        'categories': categories,
        'page_obj': page_obj,
        'sort': sort,
        'selected_category_slug': category_slug,
        'mine': mine,
        **base_context(),
    }
    return render(request, 'forum/discussion_list.html', context)


# category_discussions view is completed by me. - {{Utsav CE027}}
def category_discussions(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    discussions = category.discussions.select_related('author').all()
    sort = request.GET.get('sort', 'newest')
    if sort == 'oldest':
        discussions = discussions.order_by('created_at')
    else:
        discussions = discussions.order_by('-created_at')

    paginator = Paginator(discussions, 10)
    page_obj = paginator.get_page(request.GET.get('page', 1))
    categories = Category.objects.all()
    context = {
        'category': category,
        'discussions': page_obj,
        'categories': categories,
        'page_obj': page_obj,
        'sort': sort,
        **base_context(),
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
        **base_context(),
    }
    return render(request, 'forum/new_category.html', context)


# discussion_detail view is completed by me. - {{Utsav CE027}}
def discussion_detail(request, discussion_slug):
    discussion = get_object_or_404(Discussion, slug=discussion_slug)
    comment_sort = request.GET.get('comment_sort', 'newest')
    comments = discussion.comments.filter(parent_comment__isnull=True)
    if comment_sort == 'oldest':
        comments = comments.order_by('created_at')
    else:
        comments = comments.order_by('-created_at')

    paginator = Paginator(comments, 10)
    comments_page = paginator.get_page(request.GET.get('page', 1))
    categories = Category.objects.all()
    context = {
        'discussion': discussion,
        'comments': comments_page,
        'comments_page': comments_page,
        'comment_sort': comment_sort,
        'categories': categories,
        **base_context(),
    }
    return render(request, 'forum/discussion_detail.html', context)

# new_discussion view is completed by me. - {{Utsav CE027}}
@login_required(login_url='login')
def new_discussion(request, category_slug=None):
    categories = Category.objects.all()
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
    
    if request.method == 'POST':
        form_category_id = request.POST.get('category')
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = get_object_or_404(Category, pk=form_category_id)
        discussion = Discussion.objects.create(
            category=category,
            title=title,
            content=content,
            author=request.user,
        )
        return redirect('discussion_detail', discussion_slug=discussion.slug)
    
    context = {
        'categories': categories,
        'selected_category': selected_category,
        **base_context(),
    }
    return render(request, 'forum/new_discussion.html', context)


@login_required(login_url='login')
def edit_discussion(request, discussion_slug):
    discussion = get_object_or_404(Discussion, slug=discussion_slug)
    if discussion.author != request.user:
        messages.error(request, "You are not allowed to edit this discussion.")
        return redirect('discussion_detail', discussion_slug=discussion.slug)

    categories = Category.objects.all()
    if request.method == 'POST':
        form_category_id = request.POST.get('category')
        title = request.POST.get('title')
        content = request.POST.get('content')
        if not title or not content:
            messages.error(request, "Please fill out all fields.")
        else:
            discussion.category = get_object_or_404(Category, pk=form_category_id)
            discussion.title = title
            discussion.content = content
            discussion.save()
            messages.success(request, "Discussion updated successfully.")
            return redirect('discussion_detail', discussion_slug=discussion.slug)

    context = {
        'discussion': discussion,
        'categories': categories,
        **base_context(),
    }
    return render(request, 'forum/edit_discussion.html', context)

# delete_discussion view is completed by me. - {{Utsav CE027}}
@login_required(login_url='login')
def delete_discussion(request, discussion_slug):
    discussion = get_object_or_404(Discussion, slug=discussion_slug)
    if discussion.author == request.user:
        category_slug = discussion.category.slug
        discussion.delete()
        messages.success(request, "Discussion deleted successfully.")
        return redirect('category_discussions', category_slug=category_slug)
    else:
        messages.error(request, "You are not allowed to delete this discussion.")
        return redirect('discussion_detail', discussion_slug=discussion.slug)


# {{Ronak CE037}} - add_comment view is implemented by me.
@login_required(login_url='login')
def add_comment(request, discussion_slug):
    discussion = get_object_or_404(Discussion, slug=discussion_slug)
    if request.method == 'POST':
        text = request.POST.get('text')
        parent_id = request.POST.get('parent')
        if not text:
            messages.error(request, "Comment cannot be empty.")
            return redirect('discussion_detail', discussion_slug=discussion.slug)

        if parent_id:
            parent_comment = get_object_or_404(Comment, pk=parent_id)
            if parent_comment.discussion_id != discussion.id:
                messages.error(request, "Invalid reply target.")
                return redirect('discussion_detail', discussion_slug=discussion.slug)
            if parent_comment.parent_comment_id:
                messages.error(request, "You can only reply to top-level comments.")
                return redirect('discussion_detail', discussion_slug=discussion.slug)
            Comment.objects.create(
                discussion=discussion,
                author=request.user,
                text=text,
                parent_comment=parent_comment
            )
        else:
            Comment.objects.create(
                discussion=discussion,
                author=request.user,
                text=text
            )
        return redirect('discussion_detail', discussion_slug=discussion.slug)
    return redirect('discussion_detail', discussion_slug=discussion.slug)

# {{Ronak CE037}} - delete_comment view is implemented by me.
@login_required(login_url='login')
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.author == request.user:
        has_replies = Comment.objects.filter(parent_comment_id=comment.id).exists()
        if has_replies:
            messages.error(request, "You cannot delete a comment with replies.")
            return redirect('discussion_detail', discussion_slug=comment.discussion.slug)
        comment.delete()
        messages.success(request, "Comment deleted successfully.")
        return redirect('discussion_detail', discussion_slug=comment.discussion.slug)
    else:
        messages.error(request, "You are not allowed to delete this comment.")
        return redirect('discussion_detail', discussion_slug=comment.discussion.slug)


@login_required(login_url='login')
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.author != request.user:
        messages.error(request, "You are not allowed to edit this comment.")
        return redirect('discussion_detail', discussion_slug=comment.discussion.slug)

    if request.method != 'POST':
        return redirect('discussion_detail', discussion_slug=comment.discussion.slug)

    text = request.POST.get('text')
    if not text:
        messages.error(request, "Comment cannot be empty.")
    else:
        comment.text = text
        comment.save()
        messages.success(request, "Comment updated successfully.")
    return redirect('discussion_detail', discussion_slug=comment.discussion.slug)


# {{Ronak CE037}} - login_view, logout_view and signup_view is done by me.
def login_view(request):
    categories = Category.objects.all()
    login_error_message = None
    login_open = True
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        if not username or not password:
            login_error_message = "Please fill out all fields."
        else:
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                login_error_message = "Invalid username or password!"
    context = {
        'categories': categories,
        'login_error_message': login_error_message,
        'login_open': login_open,
        **base_context(),
    }
    return render(request, 'forum/base.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')

def signup_view(request):
    categories = Category.objects.all()
    signup_error_message = None
    signup_open = True
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        if not username or not email or not password:
            signup_error_message = "Please fill out all fields."
        elif User.objects.filter(username__iexact=username).exists():
            signup_error_message = "Username already exists!"
        elif User.objects.filter(email__iexact=email).exists():
            signup_error_message = "An account with this email already exists!"
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('home')
    
    context = {
        'categories': categories,
        'signup_error_message': signup_error_message,
        'signup_open': signup_open,
        **base_context(),
    }
    return render(request, 'forum/base.html', context)


# {{Ronak CE037}} - search function view is done by me.
def search(request):
    query = request.GET.get('q')
    discussions = Discussion.objects.filter(title__icontains=query)
    sort = request.GET.get('sort', 'newest')
    if sort == 'oldest':
        discussions = discussions.order_by('created_at')
    else:
        discussions = discussions.order_by('-created_at')

    paginator = Paginator(discussions, 10)
    page_obj = paginator.get_page(request.GET.get('page', 1))
    categories = Category.objects.all()
    context = {
        'discussions': page_obj,
        'page_obj': page_obj,
        'query': query,
        'sort': sort,
        'categories': categories,
        **base_context(),
    }
    return render(request, 'forum/search_results.html', context)


# about view is completed by me. - {{Utsav CE027}}
def about(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        **base_context(),
    }
    return render(request, 'forum/about.html', context)

