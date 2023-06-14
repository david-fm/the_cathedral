from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Block, Comments, Publication, Keywords, BlockTitle


@receiver(post_save, sender=Block)
def create_comment(sender, instance, created, **kwargs):
    if created:
        Comments.objects.create(block=instance)

@receiver(post_save, sender=Publication)
def intialize_publication(sender, instance, created, **kwargs):
    if created:
        block = Block.objects.create(publication=instance)
        block.save()
        block_title = BlockTitle(title="Empty Title", block=block)
        block_title.save()
        keywords = Keywords(publications=instance)
        keywords.save()
