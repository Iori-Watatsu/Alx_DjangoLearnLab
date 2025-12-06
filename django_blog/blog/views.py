from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Post, Comment
from .forms import PostForm, CommentForm

# Post views (unchanged)
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all().order_by('-created_at')
        context['comment_form'] = CommentForm()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Post created successfully!')
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        messages.success(self.request, 'Post updated successfully!')
        return super().form_valid(form)

    def test_func(self):
        return self.request.user == self.get_object().author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        return self.request.user == self.get_object().author

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Post deleted successfully!')
        return super().delete(request, *args, **kwargs)

# Comment views - REQUIRED BY CHECK
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/post_detail.html'

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.post = post
        form.instance.author = self.request.user
        messages.success(self.request, 'Comment added successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.kwargs['pk']})

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        messages.success(self.request, 'Comment updated successfully!')
        return super().form_valid(form)

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Comment deleted successfully!')
        return super().delete(request, *args, **kwargs)

# Home view
def home(request):
    return render(request, 'blog/home.html', {'posts': Post.objects.all().order_by('-date_posted')})

# blog/views.py (add search view and tag views)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Post, Comment, Tag  # Add Tag import
from .forms import PostForm, CommentForm, CustomUserCreationForm, ProfileUpdateForm

# Search View
def search_posts(request):
    query = request.GET.get('q', '')
    posts = Post.objects.all().order_by('-date_posted')

    if query:
        # Search in title, content, and tags
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)  # If using django-taggit
        ).distinct()

    context = {
        'posts': posts,
        'query': query,
        'results_count': posts.count()
    }
    return render(request, 'blog/search_results.html', context)

# Posts by Tag View
def posts_by_tag(request, tag_slug=None):
    tag = None
    posts = Post.objects.all().order_by('-date_posted')

    if tag_slug:
        if hasattr(Post, 'tags'):  # Using django-taggit
            posts = posts.filter(tags__slug__in=[tag_slug])
        else:  # Using custom Tag model
            tag = get_object_or_404(Tag, slug=tag_slug)
            posts = tag.posts.all().order_by('-date_posted')

    context = {
        'tag': tag,
        'posts': posts,
        'posts_count': posts.count()
    }
    return render(request, 'blog/posts_by_tag.html', context)

# Update PostDetailView to show tags in context
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all().order_by('-created_at')
        context['comment_form'] = CommentForm()

        # Get related posts by tags
        if hasattr(self.object, 'tags'):
            post_tags_ids = self.object.tags.values_list('id', flat=True)
            related_posts = Post.objects.filter(
                tags__in=post_tags_ids
            ).exclude(id=self.object.id).distinct()[:3]
            context['related_posts'] = related_posts

        return context

# Tag List View (Show all tags with post counts)
def tag_list(request):
    if hasattr(Post, 'tags'):  # Using django-taggit
        from taggit.models import Tag
        tags = Tag.objects.all().annotate(num_posts=models.Count('taggit_taggeditem_items'))
    else:  # Using custom Tag model
        tags = Tag.objects.all().annotate(num_posts=models.Count('posts'))

    # Sort by number of posts (descending)
    tags = tags.order_by('-num_posts')

    return render(request, 'blog/tag_list.html', {'tags': tags})

