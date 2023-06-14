from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Block, Comments


@receiver(post_save, sender=Block)
def create_comment(sender, instance, created, **kwargs):
    if created:
        Comments.objects.create(block=instance)
