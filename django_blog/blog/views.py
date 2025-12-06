from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils import timezone
from .models import Post, Category, Tag, Comment, Like
from .forms import PostForm, CommentForm, UserProfileForm


def home(request):
    """
Home page view displaying featured and recent posts.
    """
    # Featured posts (you can customize the logic for featured posts)
    featured_posts = Post.objects.filter(
        status=Post.Status.PUBLISHED
    ).order_by('-view_count')[:3]

    # Recent posts
    recent_posts = Post.objects.filter(
        status=Post.Status.PUBLISHED
    ).order_by('-published_date')[:6]

    # Popular categories
    popular_categories = Category.objects.annotate(
        post_count=Count('posts')
    ).order_by('-post_count')[:5]

    context = {
        'featured_posts': featured_posts,
        'posts': recent_posts,
        'popular_categories': popular_categories,
        'title': 'Home - Django Blog'
    }
    return render(request, 'blog/home.html', context)


def about(request):
    """
About page view.
    """
    return render(request, 'blog/about.html', {'title': 'About'})


def post_list(request):
    """
List all published blog posts.
    """
    posts_list = Post.objects.filter(
        status=Post.Status.PUBLISHED
    ).order_by('-published_date')

    # Pagination
    paginator = Paginator(posts_list, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'posts': page_obj.object_list,
        'is_paginated': paginator.num_pages > 1,
        'title': 'All Posts'
    }
    return render(request, 'blog/post_list.html', context)


def post_detail(request, pk=None, year=None, month=None, day=None, slug=None):
    """
Display a single blog post.
    """
    if pk:
        post = get_object_or_404(Post, pk=pk)
    else:
        post = get_object_or_404(
            Post,
            published_date__year=year,
            published_date__month=month,
            published_date__day=day,
            slug=slug,
            status=Post.Status.PUBLISHED
        )

    # Increment view count
    post.increment_view_count()

    # Get related posts
    related_posts = Post.objects.filter(
        category=post.category,
        status=Post.Status.PUBLISHED
    ).exclude(pk=post.pk)[:3]

    # Comments
    comments = post.comments.filter(is_approved=True, parent=None)

    context = {
        'post': post,
        'related_posts': related_posts,
        'comments': comments,
        'title': post.title
    }
    return render(request, 'blog/post_detail.html', context)


@login_required
def post_create(request):
    """
Create a new blog post.
    """
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # Save many-to-many relationships (tags)
            messages.success(request, 'Post created successfully!')
            return redirect(post.get_absolute_url())
    else:
        form = PostForm()

    context = {
        'form': form,
        'title': 'Create New Post'
    }
    return render(request, 'blog/post_form.html', context)


@login_required
def post_update(request, pk):
    """
Update an existing blog post.
    """
    post = get_object_or_404(Post, pk=pk)

    # Check if user is authorized to edit
    if request.user != post.author and not request.user.is_staff:
        messages.error(request, 'You are not authorized to edit this post.')
        return redirect(post.get_absolute_url())

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect(post.get_absolute_url())
    else:
        form = PostForm(instance=post)

    context = {
        'form': form,
        'post': post,
        'title': f'Update {post.title}'
    }
    return render(request, 'blog/post_form.html', context)


@login_required
def post_delete(request, pk):
    """
Delete a blog post.
    """
    post = get_object_or_404(Post, pk=pk)

    # Check if user is authorized to delete
    if request.user != post.author and not request.user.is_staff:
        messages.error(request, 'You are not authorized to delete this post.')
        return redirect(post.get_absolute_url())

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('blog:home')

    context = {
        'post': post,
        'title': f'Delete {post.title}'
    }
    return render(request, 'blog/post_confirm_delete.html', context)


@login_required
def post_like(request, pk):
    """
Like or unlike a blog post.
    """
    post = get_object_or_404(Post, pk=pk)

    # Check if user already liked the post
    like_exists = Like.objects.filter(post=post, user=request.user).exists()

    if like_exists:
        # Unlike the post
        Like.objects.filter(post=post, user=request.user).delete()
        messages.info(request, 'You unliked this post.')
    else:
        # Like the post
        Like.objects.create(post=post, user=request.user)
        messages.success(request, 'You liked this post!')

    return redirect(post.get_absolute_url())


def category_posts(request, slug):
    """
Display posts by category.
    """
    category = get_object_or_404(Category, slug=slug)
    posts_list = Post.objects.filter(
        category=category,
        status=Post.Status.PUBLISHED
    ).order_by('-published_date')

    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'page_obj': page_obj,
        'posts': page_obj.object_list,
        'is_paginated': paginator.num_pages > 1,
        'title': f'Posts in {category.name}'
    }
    return render(request, 'blog/category_posts.html', context)


def tag_posts(request, slug):
    """
Display posts by tag.
    """
    tag = get_object_or_404(Tag, slug=slug)
    posts_list = Post.objects.filter(
        tags=tag,
        status=Post.Status.PUBLISHED
    ).order_by('-published_date')

    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'tag': tag,
        'page_obj': page_obj,
        'posts': page_obj.object_list,
        'is_paginated': paginator.num_pages > 1,
        'title': f'Posts tagged with {tag.name}'
    }
    return render(request, 'blog/tag_posts.html', context)


def author_posts(request, username):
    """
Display posts by author.
    """
    author = get_object_or_404(User, username=username)
    posts_list = Post.objects.filter(
        author=author,
        status=Post.Status.PUBLISHED
    ).order_by('-published_date')

    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'author': author,
        'page_obj': page_obj,
        'posts': page_obj.object_list,
        'is_paginated': paginator.num_pages > 1,
        'title': f'Posts by {author.get_full_name() or author.username}'
    }
    return render(request, 'blog/author_posts.html', context)


@login_required
def add_comment(request, pk):
    """
Add a comment to a blog post.
    """
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user

            # Check for parent comment
            parent_id = request.POST.get('parent_id')
            if parent_id:
                parent_comment = get_object_or_404(Comment, pk=parent_id)
                comment.parent = parent_comment

            comment.save()
            messages.success(request, 'Your comment has been submitted for review.')

    return redirect(post.get_absolute_url())


def register(request):
    """
User registration view.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()

    context = {
        'form': form,
        'title': 'Register'
    }
    return render(request, 'blog/register.html', context)


@login_required
def profile(request):
    """
User profile view.
    """
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('blog:profile')
    else:
        form = UserProfileForm(instance=request.user)

    # Get user's posts
    user_posts = Post.objects.filter(author=request.user).order_by('-published_date')

    context = {
        'form': form,
        'user_posts': user_posts,
        'title': 'My Profile'
    }
    return render(request, 'blog/profile.html', context)


def search(request):
    """
Search blog posts.
    """
    query = request.GET.get('q', '')
    results = []

    if query:
        # Search in title, content, and author username
        results = Post.objects.filter(
            Q(status=Post.Status.PUBLISHED) &
            (Q(title__icontains=query) |
             Q(content__icontains=query) |
             Q(author__username__icontains=query) |
             Q(category__name__icontains=query) |
             Q(tags__name__icontains=query))
        ).distinct().order_by('-published_date')

    paginator = Paginator(results, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'query': query,
        'page_obj': page_obj,
        'results': page_obj.object_list,
        'is_paginated': paginator.num_pages > 1,
        'title': f'Search Results for "{query}"'
    }
    return render(request, 'blog/search_results.html', context)

# blog/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileUpdateForm
from django.contrib.auth.forms import AuthenticationForm

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('profile')
    else:
        form = CustomUserCreationForm()

    return render(request, 'blog/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('profile')
    else:
        form = AuthenticationForm()

    return render(request, 'blog/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'blog/profile.html', {'form': form})