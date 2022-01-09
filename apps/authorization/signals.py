from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from rest_framework.authtoken.models import Token

from utils.cache import generate_cache_key
from .models import User


@receiver(post_save, sender=User)
def invalidate_cache(sender, instance: User, created, **kwargs):
    if Token.objects.filter(user=instance).exists():
        cache_key = generate_cache_key("get-me", instance)
        cache.delete(cache_key)
