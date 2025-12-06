"""
Signal handlers for the blog application.
These signals are used to automatically perform actions when models are saved or deleted.
"""

from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from .models import Post, Comment, Like
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Post)
def create_post_slug(sender, instance, **kwargs):
    """
Automatically generate a slug for the post if it doesn't have one.
Ensures unique slugs by appending numbers if necessary.
    """
    if not instance.slug:
        # Create slug from title
        base_slug = slugify(instance.title)
        instance.slug = base_slug

        # Check if slug already exists and make it unique
        counter = 1
        while Post.objects.filter(slug=instance.slug).exclude(pk=instance.pk).exists():
            instance.slug = f"{base_slug}-{counter}"
            counter += 1


@receiver(pre_save, sender=Post)
def update_post_cache(sender, instance, **kwargs):
    """
Clear cache when a post is updated.
This ensures users see the latest content.
    """
    # Clear the cache for this post
    cache_keys = [
        f'post_{instance.pk}',
        f'post_detail_{instance.pk}',
        'recent_posts',
        'featured_posts',
        'home_page_data'
    ]

    for key in cache_keys:
        cache.delete(key)


@receiver(post_save, sender=Comment)
def send_comment_notification(sender, instance, created, **kwargs):
    """
Send notification when a new comment is created.
In a real application, this would send an email to the post author.
    """
    if created:
        logger.info(f'New comment by {instance.author} on post: {instance.post.title}')

        # Here you could add email notification logic
        # For example:
        # send_mail(
        #     f'New Comment on "{instance.post.title}"',
        #     f'{instance.author} commented: {instance.content[:100]}...',
        #     'noreply@yourblog.com',
        #     [instance.post.author.email],
        #     fail_silently=True,
        # )


@receiver(post_save, sender=Like)
def update_post_like_count(sender, instance, created, **kwargs):
    """
Update cache when a post is liked or unliked.
    """
    if created:
        # Clear cache for this post's like count
        cache.delete(f'post_{instance.post.pk}_likes')

        # Log the like action
        logger.info(f'{instance.user} liked post: {instance.post.title}')


@receiver(post_delete, sender=Like)
def update_post_unlike_count(sender, instance, **kwargs):
    """
Update cache when a like is removed.
    """
    cache.delete(f'post_{instance.post.pk}_likes')
    logger.info(f'{instance.user} unliked post: {instance.post.title}')


@receiver(post_save, sender=Post)
def publish_post_handler(sender, instance, created, **kwargs):
    """
Handle actions when a post is published.
    """
    if instance.status == Post.Status.PUBLISHED and not instance.published_date:
        # Set the published date if it's being published for the first time
        from django.utils import timezone
        instance.published_date = timezone.now()
        instance.save(update_fields=['published_date'])
        logger.info(f'Post published: {instance.title}')


@receiver(post_delete, sender=Post)
def clear_post_cache_on_delete(sender, instance, **kwargs):
    """
Clear cache when a post is deleted.
    """
    cache_keys = [
        f'post_{instance.pk}',
        f'post_detail_{instance.pk}',
        'recent_posts',
        'featured_posts',
        'home_page_data'
    ]

    for key in cache_keys:
        cache.delete(key)

    logger.info(f'Post deleted: {instance.title}')