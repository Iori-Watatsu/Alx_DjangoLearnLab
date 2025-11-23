from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Book, Post, Comment
from .forms import BookForm, PostForm, CommentForm

# Book Views

@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """View to list all books - requires can_view permission"""
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {
        'books': books
    })

@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    """View to create a new book - requires can_create permission"""
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.created_by = request.user
            book.save()
            messages.success(request, 'Book created successfully!')
            return redirect('bookshelf:book_list')
    else:
        form = BookForm()

    return render(request, 'bookshelf/book_form.html', {
        'form': form,
        'title': 'Add New Book'
    })

@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    """View to edit a book - requires can_edit permission"""
    book = get_object_or_404(Book, pk=pk)

    # Object-level permission check
    if not book.user_can_edit(request.user):
        return HttpResponseForbidden("You don't have permission to edit this book.")

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('bookshelf:book_list')
    else:
        form = BookForm(instance=book)

    return render(request, 'bookshelf/book_form.html', {
        'form': form,
        'title': 'Edit Book',
        'book': book
    })

@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    """View to delete a book - requires can_delete permission"""
    book = get_object_or_404(Book, pk=pk)

    # Object-level permission check
    if not book.user_can_delete(request.user):
        return HttpResponseForbidden("You don't have permission to delete this book.")

    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('bookshelf:book_list')

    return render(request, 'bookshelf/book_confirm_delete.html', {
        'book': book
    })

@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_detail(request, pk):
    """View to show book details - requires can_view permission"""
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'bookshelf/book_detail.html', {
        'book': book
    })

# Post Views (using the Post model from your existing code)

@login_required
@permission_required('bookshelf.can_view_post', raise_exception=True)
def post_list(request):
    """View to list all posts"""
    posts = Post.objects.all()
    return render(request, 'bookshelf/post_list.html', {
        'posts': posts
    })

@login_required
@permission_required('bookshelf.can_create_post', raise_exception=True)
def post_create(request):
    """View to create a new post"""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('bookshelf:post_list')
    else:
        form = PostForm()

    return render(request, 'bookshelf/post_form.html', {
        'form': form,
        'title': 'Create New Post'
    })

@login_required
@permission_required('bookshelf.can_edit_post', raise_exception=True)
def post_edit(request, pk):
    """View to edit a post"""
    post = get_object_or_404(Post, pk=pk)

    if not post.user_can_edit_post(request.user):
        return HttpResponseForbidden("You don't have permission to edit this post.")

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('bookshelf:post_list')
    else:
        form = PostForm(instance=post)

    return render(request, 'bookshelf/post_form.html', {
        'form': form,
        'title': 'Edit Post',
        'post': post
    })

@login_required
@permission_required('bookshelf.can_delete_post', raise_exception=True)
def post_delete(request, pk):
    """View to delete a post"""
    post = get_object_or_404(Post, pk=pk)

    if not post.user_can_delete_post(request.user):
        return HttpResponseForbidden("You don't have permission to delete this post.")

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('bookshelf:post_list')

    return render(request, 'bookshelf/post_confirm_delete.html', {
        'post': post
    })

# Comment Views

@login_required
@permission_required('bookshelf.can_create_comment', raise_exception=True)
def comment_create(request, post_pk):
    """View to create a comment on a post"""
    post = get_object_or_404(Post, pk=post_pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('bookshelf:post_list')
    else:
        form = CommentForm()

    return render(request, 'bookshelf/comment_form.html', {
        'form': form,
        'post': post,
        'title': 'Add Comment'
    })

@login_required
@permission_required('bookshelf.can_edit_comment', raise_exception=True)
def comment_edit(request, pk):
    """View to edit a comment"""
    comment = get_object_or_404(Comment, pk=pk)

    if not comment.user_can_edit_comment(request.user):
        return HttpResponseForbidden("You don't have permission to edit this comment.")

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment updated successfully!')
            return redirect('bookshelf:post_list')
    else:
        form = CommentForm(instance=comment)

    return render(request, 'bookshelf/comment_form.html', {
        'form': form,
        'title': 'Edit Comment',
        'comment': comment
    })

@login_required
@permission_required('bookshelf.can_delete_comment', raise_exception=True)
def comment_delete(request, pk):
    """View to delete a comment"""
    comment = get_object_or_404(Comment, pk=pk)

    if not comment.user_can_delete_comment(request.user):
        return HttpResponseForbidden("You don't have permission to delete this comment.")

    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment deleted successfully!')
        return redirect('bookshelf:post_list')

    return render(request, 'bookshelf/comment_confirm_delete.html', {
        'comment': comment
    })

# Dashboard view to show user-specific content
@login_required
def dashboard(request):
    """Dashboard showing user's books and posts"""
    user_books = Book.objects.filter(created_by=request.user)
    user_posts = Post.objects.filter(author=request.user)
    user_comments = Comment.objects.filter(author=request.user)

    return render(request, 'bookshelf/dashboard.html', {
        'user_books': user_books,
        'user_posts': user_posts,
        'user_comments': user_comments
    })

from .forms import ExampleForm

def example_form_view(request):
    """
View to demonstrate the ExampleForm with security best practices.
    """
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Security: Process cleaned and sanitized data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            priority = form.cleaned_data['priority']

            # Security: Log the form submission (in a real app, you might save to database)
            print(f"Security: Form submitted by {name} ({email}) with {priority} priority")

            # Security: Success message with sanitized data
            messages.success(request, f'Thank you {escape(name)}! Your message has been securely processed.')
            return redirect('bookshelf:example_form_success')
    else:
        form = ExampleForm()

    return render(request, 'bookshelf/example_form.html', {
        'form': form,
        'title': 'Example Form - Security Demonstration'
    })

def example_form_success(request):
    """
Success page after ExampleForm submission.
    """
    return render(request, 'bookshelf/example_form_success.html', {
        'title': 'Form Submitted Successfully'
    })