from .models import Category, Tag, Post


def blog_context(request):
    """
Context processor to make blog data available globally.
    """
    context = {
        'categories': Category.objects.all(),
        'popular_tags': Tag.objects.all()[:10],
    }

    # Add recent posts for sidebar if on blog pages
    if request.resolver_match and request.resolver_match.app_name == 'blog':
        context['recent_posts'] = Post.objects.filter(
            status=Post.Status.PUBLISHED
        ).order_by('-published_date')[:5]

        context['recent_comments'] = Post.objects.filter(
            comments__is_approved=True
        ).distinct().order_by('-comments__created_at')[:5]

    return context