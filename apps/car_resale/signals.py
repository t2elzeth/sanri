from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CarResale


@receiver(post_save, sender=CarResale)
def update_stock(instance, **kwargs):
    instance.calculate_income()
