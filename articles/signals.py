from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Block, Comments, Publication, Keywords, BlockTitle


@receiver(post_save, sender=Block)
def create_comment(sender, instance, created, **kwargs):
    """ 
    Creates a comment for a block when a block is created

    :param sender: The model class
    :type sender: Block
    :param instance: The instance of the model class
    :type instance: Block
    :param created: Whether the instance was created or not
    :type created: bool
    :param kwargs: The keyword arguments
    :type kwargs: dict
    """
    if created:
        Comments.objects.create(block=instance)

@receiver(post_save, sender=Publication)
def intialize_publication(sender, instance, created, **kwargs):
    """
    
    Creates a block, block title, and keywords for a publication when a publication is created
    """
    if created:
        block = Block.objects.create(publication=instance)
        block.save()
        block_title = BlockTitle(title="Empty Title", block=block)
        block_title.save()
        keywords = Keywords(publications=instance)
        keywords.save()
