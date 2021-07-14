from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import Container, CountAndSum


@receiver(pre_save, sender=Container)
def update_stock(instance: Container, **kwargs):
    instance.calculate_total()


@receiver(post_save, sender=Container)
def post_save_car_resale(instance: Container, created, **kwargs):
    if created:
        instance.save()


@receiver(post_save, sender=CountAndSum)
def create_cound_and_sum(instance, created, **kwargs):
    if created:
        instance.container.save()
